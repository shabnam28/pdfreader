Workspace
(rerun without)
Collecting workspace information

This code is designed to process scanned PDF files, extract text using Google Document AI, and then use a Gemini model to extract structured information from the text. Finally, it saves the extracted data into a CSV file. Here's a step-by-step explanation:

Step-by-Step Explanation
1. Configuration]
    Purpose: Sets up environment variables for Google Cloud services.
2. Initialize Vertex AI
3. Prepare Gemini Model
4. Build Prompt for Gemini
5. Extract Text from PDF
8. Save Data to CSV
   
Enable Document AI API:

Go to the Google Cloud Console.
Enable the "Document AI API" for your project.
Create a Processor:

    1. Navigate to the Document AI section in the Cloud Console.
    2. Click "Create Processor."
    3.Choose "Document OCR" as the processor type.
    4.Select the region (e.g., us or eu).
    5. Note the Processor ID and Location for use in your code.
    6.Set Up Authentication:
    7.Create a service account with the "Document AI Editor" role.
    8.Download the service account key as a JSON file.
    
Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of this JSON file in envirement document.
Once configured, the code should work seamlessly with your Google Cloud setup.

