import os
from mcp.server.fastmcp import FastMCP
import xmlrpc.client

# Create MCP server
mcp = FastMCP("harmonyx-odoo")

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USER = os.getenv("ODOO_USER")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

@mcp.tool()
def search_contacts(name: str = None):
    """Search for contacts in Odoo"""
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
    
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    
    domain = []
    if name:
        domain.append(('name', 'ilike', name))
    
    partners = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'res.partner', 'search_read',
        [domain],
        {'fields': ['name', 'email', 'phone'], 'limit': 5}
    )
    
    return {"contacts": partners}