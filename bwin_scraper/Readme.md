##  Installation Steps 
1. Unzip the folder

2. Install dependencies: 
	( create a virtual env using `python -m venv venv` and activate venv in the directory) 
	`pip install -r requirements.txt`
3. Run script:
	`python main.py`
4. Output will be generated in the "Output" folder. 
	There are 3 outputs. 
		1. **raw.json** - (fixtures raw from response) - for testing
		2. **final.csv** - (csv formatted required output)
		3. **final.json** - (required output in json)

5. Logs will be generated in the "logs" folder.
	`logs` dir will be automatically created at runtime. 
	logs will be separated daily. Each day will have a folder. 
	log files will be generated each hour and saved in respective day's folder. 
	


## Further improvements:
1. Using concurrency in `process_fixtures` function of scraper module. 
2. Names are in long format. Create function to skim first names of players. 
3. `x-bwin-accessid` and `proxy` as env variables. 
4. Headers should be random from a list of headers
