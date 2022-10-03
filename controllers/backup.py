
class Restapi(http.Controller):
    # @http.route('/restapi/restapi', auth='public')
    # def index(self, **kw):
    # 	sale_order = http.request.env['sale.order'].search([])
    # 	output = '<ul>'

    # 	for sale in sale_order:
    # 		print(sale['name'])
    # 		output += '<li>' + sale['name'] + '</li>'

    # 	output += '</ul>'

    # 	return output


    @http.route('/restapi/test', auth='public')
    def index(self, **kw):
    	
    	#

    	url = 'http://localhost:8069/'
    	db = 'latihan'
    	username = 'admin'
    	password = 'admin'

    	common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    	uid = common.authenticate(db, username, password, {})
    	if uid:
    		models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    		partners = models.execute_kw(db, uid, password, 'res.partner', 'search', [[]])
    		partners_rec = models.execute_kw(db, uid, password, 'res.partner', 'read', [partners], {'fields': ['id', 'name']})
    		

    		newData = {'id': 999, 'name': 'Ivan Dwi'}

    		partners_rec.append(newData)

    		print(partners_rec)





    		sale_order = http.request.env['res.partner'].search([])

    		for partner in partners_rec:
    			check = False
    			for sale in sale_order:
    				#print('..........', sale['id'], ' / ', partner['id'])
    				if (sale['id'] == partner['id']):
    					check = True

    			if check == False:
    				print('Buat Data Baru')
    				# Create data if not match found
    				#id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': partner['name']}])


    			else:
    				print('Data Masih Ada')




    	return 'Starting'

    @http.route('/restapi/restapi/objects', auth='public')
    def list(self, **kw):
        return http.request.render('restapi.listing', {
            'root': '/restapi/restapi',
            'objects': http.request.env['restapi.restapi'].search([]),
        })

    @http.route('/restapi/restapi/objects/<model("restapi.restapi"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('restapi.object', {
            'object': obj
        })