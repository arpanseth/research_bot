# RESEARCH BOT

A simple flask app that lets users chat with their data. 

To run the app, users must set **OPENAI_API_KEY** environment variable, which can be obtained from OpenAI. Please contact Arpan Seth (aseth42@gmail.com) for further instructions. 

The app has been tested on M1 Macbook Air running Python version 3.11.9. 

Steps to run the application:

### 1. Create virtual environment and install python packages:
```
pip install -r requirements.txt
```
### 2. Setup you OpenAI API Ket environment variable:
If you haven't already, please get an API key from OpenAI and set it as you environment variable. Please contact Arpan Seth(aseth42@gmail.com) for the keys related to custom fine-tuned models. You can set the API KEY using the command:
```
export OPENAI_API_KEY='your-key-here'
```   
### 3. Load and index pdf documents for RAG:
The applicaiton supports context retreival from ingested pdf files. First, copy all pdf files you need indexed into the folder called "pdfs". Then run the following script to create the embeddings:
```
python index.py
```
You can run the above script anytime you add new pdf files to the "pdfs" folder and it will automatically process new files.   
### 4. If needed, modify the system message:
The system message lets you provide additional information to the chatbot that is included in every conversation. Users can modify the system message by editing the "system_message.txt" file.
### 5. Run the flask app:
Run the flask applicaiton with the following command:
```
python app.py
```
The application should me available through your browser at http://127.0.0.1:5000

**Note:** You can try using a different model by changing the MODEL_NAME parameter in app.py.

