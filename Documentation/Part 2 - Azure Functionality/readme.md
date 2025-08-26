# First lets make an Event Hub

I prefer to make it through VS codes portal becuase it sets up a template that will help us later

To start make a function folder from the root directory called functions.

For the next part you will need to have Azure's VS code installation. Make sure you download these

<img width="1467" height="695" alt="image" src="https://github.com/user-attachments/assets/ec247c36-e12e-4f8d-8f4d-b6590d1dc825" />

Now press ctrl+shift+p and type in azure functions create new project.

# Browse to your function folder
<img width="770" height="85" alt="image" src="https://github.com/user-attachments/assets/27d046c4-f07e-4796-bb2b-3a695f036aad" />

# Select Python
I am most comfortable coding in python. Cloud is already complicated enough :)

<img width="747" height="254" alt="image" src="https://github.com/user-attachments/assets/8ef62420-d945-4a2f-bd67-14817093fafd" />

# Select interperter. I use python 3.11
<img width="725" height="118" alt="image" src="https://github.com/user-attachments/assets/58738b1b-4369-45c8-ba4b-b596a99e3f9a" />

# Select Event Hub Trigger
We are going to need this becuase we are going off of the event of when our IoT hub recieves a message from the PI

<img width="729" height="321" alt="image" src="https://github.com/user-attachments/assets/188a0bbe-9ae3-4470-b79f-9f889eeed723" />

# Name it this
<img width="775" height="78" alt="image" src="https://github.com/user-attachments/assets/2e9aa01a-a3b3-4e4a-bf10-48474dfb7fc6" />

# Name the next part this
<img width="751" height="107" alt="image" src="https://github.com/user-attachments/assets/38c2b018-cead-4bc5-b2dc-fd67d6722d5f" />

# finally call the event hub this
<img width="753" height="88" alt="image" src="https://github.com/user-attachments/assets/dcbbc146-ce58-4624-8871-87466407ecaf" />

# Should look like this when finished
<img width="1912" height="1035" alt="image" src="https://github.com/user-attachments/assets/8f242a49-e2ba-40f0-b0ae-877d0c87dace" />

# Next go to your IoT hub and go to Message Routing.

<img width="1764" height="878" alt="image" src="https://github.com/user-attachments/assets/dca9c859-55d6-4cdd-a456-9a7cb19fba93" />

Create a routing path to your event hub.

Now you should be reciving messages to your Event Hub

<img width="1754" height="1200" alt="image" src="https://github.com/user-attachments/assets/0cc925d0-9370-4c5c-872b-742b8c11c50a" />

# Next up create an Azure Cosmos Database.
I used nosql becuase I found that eaiser to do.
<img width="1920" height="1140" alt="Screenshot 2025-08-16 152137" src="https://github.com/user-attachments/assets/7bb4e919-d03a-4133-8949-3140f009051d" />

These are the settings I used

<img width="1920" height="1140" alt="Screenshot 2025-08-16 153134" src="https://github.com/user-attachments/assets/8185b61c-8f23-4b8d-a04b-5f6fd685d4c8" />

Now open the Azure Cosmos DB in Data Explorer

<img width="1711" height="1561" alt="Screenshot 2025-08-19 115008" src="https://github.com/user-attachments/assets/39b13038-4f1f-46ef-b0c7-9d453edfe161" />

These are the settings I used for the Database. I made a change to the code where I changed the name to 
```bash
"WeatherReadingDb"
```
 Not 
 
 ```bash
"WeatherReadingsDb"
```

Once made, go into your Keys so that we can give permission to your function to add data to the table we just made

<img width="1711" height="1561" alt="Screenshot 2025-08-19 122917" src="https://github.com/user-attachments/assets/1ff921ef-e2a1-42f8-953c-1c9ca9a52dda" />

Add the string to CosmosDbConnection in your local.settings.json file.

Now that the connections are working you should be able to run the function locally using

```bash
func start
```
