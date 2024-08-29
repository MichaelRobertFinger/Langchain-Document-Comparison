## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up your Azure OpenAI API credentials:
   - Create a `.env` file in the project root.
   - Add your Azure OpenAI API details:
     ```
     AZURE_OPENAI_ENDPOINT=your_azure_endpoint
     AZURE_OPENAI_API_KEY=your_azure_api_key
     AZURE_OPENAI_DEPLOYMENT_NAME=your_gpt4_deployment_name
     ```

3. Run the Streamlit app:
   ```
   streamlit run app/main.py
   ```

4. Upload two documents (PDF or TXT), enter a comparison prompt, and click "Compare Documents" to see the results.