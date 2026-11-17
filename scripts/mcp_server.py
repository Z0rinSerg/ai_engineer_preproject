from fastmcp import FastMCP

mcp = FastMCP("AI Engineer Tools")

def register_tools():
    """Явная регистрация всех инструментов сервера"""
    
    @mcp.tool()
    def hello(name: str) -> str:
        """Приветствие пользователя"""
        return f"Hello, {name}! MCP server is running."

# Регистрируем инструменты сразу при загрузке модуля
register_tools()

if __name__ == "__main__":
    mcp.run()