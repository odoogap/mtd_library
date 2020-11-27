import odoorpc


def open_connection_odoogap(user, password, server, db, port):
    try:
        # odoo_instance = odoorpc.ODOO(server, protocol='jsonrpc+ssl', port=int(port))
        odoo_instance = odoorpc.ODOO(server, protocol='jsonrpc', port=int(port))
        odoo_instance.login(db, user, password)
            
        return odoo_instance

    except Exception as e:
        raise UserError('Invalid user.')

