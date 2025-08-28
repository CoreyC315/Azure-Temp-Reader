# Now that our IoT device is getting the temperature and adding that info to our Cosmos DB lets deploy it to a frontend so that we can see the temperature that it is reading!

Create a SignalR in Azure
These are the settings I used
<img width="1642" height="1250" alt="image" src="https://github.com/user-attachments/assets/bc337736-a9a4-40e2-a223-28920d2817b2" />

Once the SignalR has been made go to your settings and go to Keys and get your connection String

<img width="1759" height="1231" alt="image" src="https://github.com/user-attachments/assets/f42ef30e-c2d5-422e-a1b3-67c66856bd95" />

Make sure that it is in your local.settings.json file following the Template

Use this extension to make a live server easily
<img width="1435" height="1278" alt="image" src="https://github.com/user-attachments/assets/7bb22983-50d2-4a39-81c4-b67e2ace7e19" />

Start a live server
<img width="520" height="744" alt="image" src="https://github.com/user-attachments/assets/e5b287c5-90f3-4032-9a96-2edd4365e002" />

If run locally it will start up and will start taking measurements for the temperature and the humidity.

Make sure that CORS is updated for your IP in the host.json file so that the API can pull from it.
