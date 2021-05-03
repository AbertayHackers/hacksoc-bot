# Hacksoc Bot
## Discord bot for the Abertay Hacksoc [Discord Server](https://discord.hacksoc.co.uk)

## Contributions Policy
Contributions from Hacksoc members are welcome! 

Please feel free to fork the public repo to create your own development repo. If you wish to add this into the Hacksoc bot dev server, please speak to the secretary.

When deploying:
* Go to the [Discord Developer portal](https://discord.com/developers/) and create a bot. Take note of the token!
* Clone your local copy of the repository to a development machine (a linux VM is ideal for this, as you can also create a MySQL Database)
*  `config/secrets.json` file (there is a template provided at `config/secrets.json.template`). This should include:
	* Credentials for a local MySQL Database
	* The Bot Token you noted down earlier
* Initialise your MySQL database locally by running the `init.sql` script.
* Run the `main.py` script.
* Your bot should now be deployed!
