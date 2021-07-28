# Hacksoc Bot
## Discord bot for the Abertay Hacksoc [Discord Server](https://discord.hacksoc.co.uk)

## Contributions Policy
Contributions from Hacksoc members are welcome! 

Please feel free to fork the public repo to create your own development repo. If you wish to add this into the Hacksoc bot dev server, please speak to the secretary.

When deploying:
* Go to the [Discord Developer portal](https://discord.com/developers/) and create a bot. Take note of the token!
* Clone your local copy of the repository to a development machine (a linux VM is ideal for this, as you can also create a MySQL Database)
* Create a `config/secrets.json` file (there is a template provided at `config/secrets.json.template`). You will need to fill in all of the fields in this template as directed.
* Update channel/guild IDs in the "env" section of the `config/config.json` file. A pre-populated version of this already exists for the official dev server (speak to the secretary about getting access)
* Initialise your MySQL database locally by running `mysql < config/init.sql` -- make sure to update the password!.
* Run the `main.py` script.
* Your bot should now be deployed!


## To Do:
- [ ] Add Multi-language support
- [ ] Set up decent logging
- [ ] Add AGM Commands
