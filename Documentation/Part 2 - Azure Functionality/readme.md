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

Now that we have those running you should have 3 resources.

<img width="1709" height="1132" alt="Screenshot 2025-08-18 145050" src="https://github.com/user-attachments/assets/0ebd7a07-0a4c-43e2-92e4-f47778a07bb5" />

