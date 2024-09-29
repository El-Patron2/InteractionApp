# InteractionApp
ConversAI is an intelligent companion application that leverages Google Cloud's Speech-to-Text and Text-to-Speech APIs to provide voice interaction capabilities. The application allows users to transcribe audio recordings and generate speech from text input.
Frontend:
• Simple HTML interface (index.html) for user interaction
• JavaScript likely handles API calls to the backend
Backend:
• Built using Flask, a lightweight Python web framework
• Deployed on Google Cloud Run, a serverless platform for containerized applications
• Utilizes Google Cloud Speech-to-Text and Text-to-Speech APIs for core functionality
Key Components:
Flask application setup with CORS enabled
Google Cloud API client initialization using service account credentials
Two main routes: /transcribe for speech-to-text and /generate-speech for text-to-speech
Comprehensive error handling and logging
Deployment
The application is successfully deployed on Google Cloud Run:
• Service Name: conversai
• Revision: conversai-00003-zq6
• Service URL: https://conversai-407890873479.us-central1.run.app
This serverless deployment allows for easy scaling and management of the application.
