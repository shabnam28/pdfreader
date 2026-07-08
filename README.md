## 1.1 Overview
Collecting workspace information

This code is designed to process scanned PDF files, extract text using Google Document AI, and then use a Gemini model to extract structured information from the text. Finally, it saves the extracted data into a CSV file. Here's a step-by-step explanation:

---

## 1.2 Workflow Steps:
Step-by-Step Explanation
1. Configuration]
    Purpose: Sets up environment variables for Google Cloud services.
2. Initialize Vertex AI
3. Prepare Gemini Model
4. Build Prompt for Gemini
5. Extract Text from PDF
8. Save Data to CSV

<img src="./assets/image.svg" alt="Architecture Diagram" width="900"/>
 
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

---
## Estimated Processing Cost

The following estimate is based on processing **2,000 PDF documents** (~**14,000 pages**) using **Google Document AI OCR** and **Gemini 2.5 Pro**.

---

## 2.1 Google Document AI (OCR) Cost

**Total pages:** 14,000

| Pricing Model | Calculation | Estimated Cost |
|---|---|---:|
| $1.50 per 1,000 pages | 14,000 / 1,000 × $1.50 | ~$21.00 |
| $0.60 per 1,000 pages | 14,000 / 1,000 × $0.60 | ~$8.40 |

**Estimated OCR cost: ~$8.40 - $21.00**

---

## 2.2 Gemini 2.5 Pro Cost

### Assumptions

- Number of documents: **2,000**
- Average document size: **7 pages**
- Average extracted text: **3,000 French words/document**
- Token estimation: **0.75 words/token**
- Input tokens per document: **~2,250 tokens**
- Output JSON response: **~100 tokens/document**

---

### Token Calculation

| Type | Calculation | Total Tokens |
|---|---|---:|
| Input tokens | 2,000 documents × 2,250 tokens | 4,500,000 tokens |
| Output tokens | 2,000 documents × 100 tokens | 200,000 tokens |

---

### Gemini 2.5 Pro Pricing

| Token Type | Price |
|---|---:|
| Input tokens | $1.25 / 1M tokens |
| Output tokens | $5.00 / 1M tokens |

---

### Estimated Gemini Cost

| Component | Calculation | Cost |
|---|---|---:|
| Input | 4.5M × $1.25 / 1M | ~$5.63 |
| Output | 0.2M × $5 / 1M | ~$1.00 |

**Estimated Gemini Cost: ~$6.63**

---

## 2.3 Total Estimated Service Cost

| Scenario | Document AI | Gemini | Total |
|---|---:|---:|---:|
| Lower estimate | $8.40 | $6.63 | **~$15.03** |
| Higher estimate | $21.00 | $6.63 | **~$27.63** |

---

## 2.4 Final Estimate

Processing **2,000 documents (~14,000 pages)** is expected to cost approximately:

**💰 $15 - $28 USD**

> Note: Actual costs may vary depending on document complexity, OCR output size, extracted text length, and generated JSON response size.
    
Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of this JSON file in envirement document.
Once configured, the code should work seamlessly with your Google Cloud setup.

