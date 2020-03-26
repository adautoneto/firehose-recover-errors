import psycopg2
import yaml

with open('firehose.yaml', 'r') as f:
	  config = yaml.full_load(f)

def copy(conn, manifest):
	try:

		cursor = conn.cursor()
		cfg = config["copy"]
		copy_command = ("COPY " + cfg["table"] 
			+ " FROM 's3://" + cfg["bucket"] + "/" + manifest.strip() 
			+ "' CREDENTIALS '" + cfg["credentials"] 
			+ "' MANIFEST " + cfg["options"] + ";")
		print(copy_command)
		cursor.execute(copy_command)
		conn.commit()

	except Exception as ex:
		print("Failed to copy manifest file {0}. Error: {1}".format(manifest,ex))

try:
		cfg = config["redshift"]

		# Database connection below that uses the DbPassword that boto3 returned
		conn = psycopg2.connect(
										host = cfg["host"],
										port = cfg["port"],
										user = cfg["user"],
										password = cfg["password"],
										database = cfg["database"]
										)

		# Print PostgreSQL version
		cursor = conn.cursor()
		cursor.execute("SELECT version();")
		record = cursor.fetchone()
		print("You are connected to - ", record,"\n")

		with open('manifests.txt') as f:
			for line in f:
				copy(conn, line)
		
		conn.close()

except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)