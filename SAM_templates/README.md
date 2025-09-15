# JEDx Phase II Pilot – Reference Templates

> **Note**  
> - These are artifacts for **JEDx Phase II Pilot**  
> - Not meant for production  
> - Questions can be sent to **Jim Goodell (jimgoodell@qi-partners.com)** and **Alex Jackl (alex@bardicsystems.com)**

---

This folder contains reference templates for the **JEDx CAR and Collector services**, designed to support rapid setup and understanding of the serverless architecture.

- **Quickstart Guides** (CAR and Collector) provide a high-level overview of parameters, core resources (S3, DynamoDB, Kinesis, API Gateway, Lambda), and the data flow from ingestion through validation:  
  - `car_template_quickstart`  
  - `collector_template_quickstart`  

- **Walkthrough Guides** expand on these by describing each AWS SAM resource in plain English, including how the APIs, pipelines, and storage layers interact, with notes on monitoring, IAM scoping, and deployment considerations:  
  - `car_template_walkthrough`  
  - `collector_template_walkthrough`  
