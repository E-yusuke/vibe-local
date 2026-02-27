"""
Additional tool implementations for SQLite and Excel file handling.
"""

import json
import os
import sqlite3
from abc import ABC, abstractmethod


class ToolResult:
    """Result from a tool invocation."""
    
    def __init__(self, output="", error="", exit_code=0):
        self.output = output
        self.error = error
        self.exit_code = exit_code


class Tool(ABC):
    """Base class for tools."""
    
    @property
    @abstractmethod
    def definition(self):
        """Return OpenAI-compatible tool definition."""
        pass
    
    @abstractmethod
    def invoke(self, **kwargs):
        """Invoke the tool. Returns ToolResult."""
        pass


class SQLiteTool(Tool):
    """Execute SQL queries against SQLite databases."""
    
    def __init__(self, db_folder=None):
        """
        Args:
            db_folder: Folder containing SQLite database files.
                      If None, defaults to user's data folder.
        """
        if db_folder is None:
            db_folder = os.path.expanduser("~/AppData/Local/vibe-local/data")
            if not os.path.exists(db_folder):
                db_folder = os.path.expanduser("~/.local/share/vibe-local/data")
        self.db_folder = db_folder
        os.makedirs(db_folder, exist_ok=True)
    
    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": "sqlite_query",
                "description": "Execute a SQL query against a SQLite database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "database": {
                            "type": "string",
                            "description": "Database filename (without path, e.g., 'app.db')"
                        },
                        "query": {
                            "type": "string",
                            "description": "SQL query to execute (SELECT, INSERT, UPDATE, DELETE, CREATE, etc.)"
                        },
                        "params": {
                            "type": "array",
                            "description": "Parameters for parameterized queries (optional)",
                            "items": {}
                        }
                    },
                    "required": ["database", "query"]
                }
            }
        }
    
    def invoke(self, database, query, params=None):
        """Execute a SQL query."""
        try:
            # Sanitize database name to prevent path traversal
            if "/" in database or "\\" in database or database.startswith("."):
                return ToolResult(
                    error=f"❌ Invalid database name: {database}\n"
                          f"  Database names must not contain path separators or dots.",
                    exit_code=1
                )
            
            db_path = os.path.join(self.db_folder, database)
            
            # Ensure the database file is in the allowed folder
            real_path = os.path.abspath(db_path)
            real_folder = os.path.abspath(self.db_folder)
            if not real_path.startswith(real_folder):
                return ToolResult(
                    error="❌ Path traversal detected. Database must be in the data folder.",
                    exit_code=1
                )
            
            # Note: SQLite will create the database file automatically on first connection
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # Check if this is a SELECT query
                if query.strip().upper().startswith("SELECT"):
                    rows = cursor.fetchall()
                    result = [dict(row) for row in rows]
                    if not result:
                        output = "No results"
                    else:
                        output = json.dumps(result, indent=2, default=str, ensure_ascii=False)
                else:
                    # For INSERT, UPDATE, DELETE, etc.
                    conn.commit()
                    output = f"✓ Query executed successfully. Rows affected: {cursor.rowcount}"
                
                return ToolResult(output=output)
            except sqlite3.Error as e:
                return ToolResult(
                    error=f"❌ SQL error: {str(e)}\n"
                          f"  Query: {query[:100]}...",
                    exit_code=1
                )
            finally:
                cursor.close()
                conn.close()
        except Exception as e:
            return ToolResult(
                error=f"❌ Database error: {str(e)}",
                exit_code=1
            )


class ExcelTool(Tool):
    """Read and analyze Excel files."""
    
    def __init__(self, excel_folder=None):
        """
        Args:
            excel_folder: Folder containing Excel files.
                         If None, defaults to user's documents folder.
        """
        if excel_folder is None:
            excel_folder = os.path.expanduser("~/AppData/Local/vibe-local/excel")
            if not os.path.exists(excel_folder):
                excel_folder = os.path.expanduser("~/Documents")
        self.excel_folder = excel_folder
        os.makedirs(excel_folder, exist_ok=True)
        
        # Try to import openpyxl/pandas, but don't fail if unavailable
        try:
            import openpyxl
            self.openpyxl = openpyxl
        except ImportError:
            self.openpyxl = None
        
        try:
            import pandas as pd
            self.pandas = pd
        except ImportError:
            self.pandas = None
    
    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": "read_excel",
                "description": "Read and analyze Excel files",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Excel filename (with .xlsx extension)"
                        },
                        "sheet": {
                            "type": "string",
                            "description": "Sheet name (optional, defaults to first sheet)"
                        },
                        "action": {
                            "type": "string",
                            "enum": ["list_sheets", "read", "summary"],
                            "description": "Action to perform (default: read)"
                        },
                        "rows": {
                            "type": "integer",
                            "description": "Number of rows to read (default: all)"
                        }
                    },
                    "required": ["filename"]
                }
            }
        }
    
    def invoke(self, filename, sheet=None, action="read", rows=None):
        """Read Excel file."""
        try:
            if not self.pandas and not self.openpyxl:
                return ToolResult(
                    error="❌ Required libraries not installed.\n"
                          "  Run: pip install pandas openpyxl",
                    exit_code=1
                )
            
            # Sanitize filename
            if "/" in filename or "\\" in filename or filename.startswith("."):
                return ToolResult(
                    error=f"❌ Invalid filename: {filename}\n"
                          f"  Filenames must not contain path separators.",
                    exit_code=1
                )
            
            file_path = os.path.join(self.excel_folder, filename)
            
            # Ensure the file is in the allowed folder
            real_path = os.path.abspath(file_path)
            real_folder = os.path.abspath(self.excel_folder)
            if not real_path.startswith(real_folder):
                return ToolResult(
                    error="❌ Path traversal detected. Files must be in the Excel folder.",
                    exit_code=1
                )
            
            if not os.path.exists(file_path):
                return ToolResult(
                    error=f"❌ File not found: {filename}\n"
                          f"  Location: {file_path}\n"
                          f"  Put Excel files in: {self.excel_folder}",
                    exit_code=1
                )
            
            if action == "list_sheets":
                return self._list_sheets(file_path)
            elif action == "summary":
                return self._get_summary(file_path, sheet)
            else:  # read
                return self._read_sheet(file_path, sheet, rows)
        
        except Exception as e:
            return ToolResult(
                error=f"❌ Error reading Excel file: {str(e)}",
                exit_code=1
            )
    
    def _list_sheets(self, file_path):
        """List all sheets in the workbook."""
        if self.openpyxl:
            try:
                wb = self.openpyxl.load_workbook(file_path, read_only=True)
                sheets = wb.sheetnames
                output = json.dumps({"sheets": sheets}, indent=2)
                wb.close()
                return ToolResult(output=output)
            except Exception as e:
                return ToolResult(error=str(e), exit_code=1)
        elif self.pandas:
            try:
                sheets = self.pandas.ExcelFile(file_path).sheet_names
                output = json.dumps({"sheets": sheets}, indent=2)
                return ToolResult(output=output)
            except Exception as e:
                return ToolResult(error=str(e), exit_code=1)
    
    def _get_summary(self, file_path, sheet):
        """Get summary statistics of a sheet."""
        if not self.pandas:
            return ToolResult(
                error="pandas required for summary. Install with: pip install pandas",
                exit_code=1
            )
        
        try:
            df = self.pandas.read_excel(file_path, sheet_name=sheet, nrows=5)
            summary = {
                "shape": list(df.shape),
                "columns": list(df.columns),
                "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "sample_rows": df.head().to_dict(orient="records")
            }
            output = json.dumps(summary, indent=2, default=str)
            return ToolResult(output=output)
        except Exception as e:
            return ToolResult(error=str(e), exit_code=1)
    
    def _read_sheet(self, file_path, sheet, rows):
        """Read sheet data."""
        if not self.pandas:
            return ToolResult(
                error="pandas required. Install with: pip install pandas",
                exit_code=1
            )
        
        try:
            df = self.pandas.read_excel(file_path, sheet_name=sheet, nrows=rows)
            # Convert to JSON-friendly format
            data = {
                "columns": list(df.columns),
                "rows": df.to_dict(orient="records")
            }
            output = json.dumps(data, indent=2, default=str)
            return ToolResult(output=output)
        except Exception as e:
            return ToolResult(error=str(e), exit_code=1)
