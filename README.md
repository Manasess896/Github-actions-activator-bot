# Github-actions-activator-bot
This is a bot that activates github actions workflow after it limit of 6 hours hence bypassing the limit and making the workflow almost run for 24 hours 
    as we all know github only keeps a live action for 6 hours .this bot and its workflow have been programmed to start your workflow at 00:00 ,then +6 hours from there therefore making your bot almost always online .
   Upon activation after 6 hours The bot runs 5 minutes after it has been activated hence to allow the previous session to complete and start a new session .
   what you will neneed is add your 
     -github token from github API 
     -the creators username 
     -the Repository name.the repo you wish to automate with this bot
     -The yml file name of the Repository

save the secrets using the following format in order for them to be properly acceessed by the yml and main.py files 
   -"TOKEN" (this is your token from github)
   -"REPO_OWNER" (this is the username of the owner of the repo you wish to automate github actions )
   -"REPO_NAME" (this is the name of the repository you wish to automate its github workflow)
   -"WORKFLOW_ID" (this is the name of your workflow or yml file e.g 'python-app.yml')

   If you dont understand this instructions i have created a .env file above use the same format to input your github secrets for this code
   HAPPY CODING
     
