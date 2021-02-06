import requests, csv, time, config

def get_toggl_data(s, e, dir_path):

	#Set Values
	key = config.api_key
	my_email = config.my_email
	add_user = f'&user_agent={my_email}'
	start = f'&since={s}'
	end = f'&until={e}'

	workspaces_endpoint = r'https://api.track.toggl.com/api/v8/workspaces'
	reports_endpoint = r'https://api.track.toggl.com/reports/api/v2/details'

	def parse_json(workspace, data):

		field_names = ['User', 'Email', 'Client', 'Project',
					   'Description', 'Start Date', 'Start Time',
					   'End Date', 'End Time', 'Duration', 'Tags']

		emails = {config.name_1: config.email_1,
				  config.name_2: config.email_2, 
				  config.name_3: config.email_3,
				  config.name_4: config.email_4,
				  config.name_5: config.email_5,
				  config.name_6: config.email_6,
				  config.name_7: config.email_7
		}

		with open(dir_path + '/' + workspace + '.csv', "w", newline='') as file:
			w = csv.DictWriter(file, field_names)
			w.writeheader()
			
			for i in data:
				data_dict = dict()

				sd = i['start'].split('T')[0]
				st = i['start'].split('T')[1][0:8]

				ed = i['end'].split('T')[0]
				et = i['end'].split('T')[1][0:8]

				email = emails[i['user']]

				data_dict['User'] = i['user']
				data_dict['Email'] = email
				data_dict['Client'] = i['client']
				data_dict['Project'] = i['project']
				data_dict['Description'] = i['description']
				data_dict['Start Date'] = sd
				data_dict['Start Time'] = st
				data_dict['End Date'] = ed
				data_dict['End Time'] = et
				data_dict['Duration'] = i['dur']/3600000
				data_dict['Tags'] = ', '.join(i['tags'])

				w.writerow(data_dict)
		


	# Get Workspace IDs
	R = requests.get(workspaces_endpoint, auth=(key, 'api_token'))

	workspace_ids = dict()
	for workspace in R.json():
		workspace_ids[workspace['name']] = workspace['id']



	# By Workspace - Get Weekly Reports
	workspace_records = dict()

	for name, id_val in workspace_ids.items():
		# if name in wspaces:
		add_id = f'?workspace_id={id_val}'

		json_corpus = list()
		i = 0
		page = 1

		while True:
			add_page = f'&page={page}'
			time.sleep(1)
			R = requests.get(reports_endpoint + add_id + add_user + start + end + add_page, auth=(key, 'api_token'))
			total = R.json()['total_count']
			i+=R.json()['per_page']
			json_corpus = json_corpus + R.json()['data']

			if i>=total:
				break
			else:
				i+=1
				page+=1

		parse_json(workspace=name, data=json_corpus)
