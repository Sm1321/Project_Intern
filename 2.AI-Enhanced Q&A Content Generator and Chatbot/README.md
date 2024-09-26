### Project Title: AI-Enhanced Q&A Content Generator and Chatbot
Project Summary: Automated Content Generation for University Courses


Business Problem:

- Universities face a significant challenge in generating high-quality, on-demand content, particularly questions for various courses. The manual creation of this content is not only time-consuming but also labor-intensive, diverting educators' focus from their primary teaching responsibilities.

Business Objective:

- The project's primary aim is to automate the Q&A creation process, maximizing the quality of generated content while minimizing the time required for its production.

Business Constraint:

- A critical constraint of this project is to minimize plagiarism in the generated content, ensuring that all questions are unique and original.

Success Criteria:

- Business Success Criteria: Achieve a reduction in content generation time by up to 80%.

- ML Success Criteria: Maintain a duplication rate of generated questions at less than 5%.

- Economic Success Criteria: Increase revenue from online-based courses by 15% in the first semester following implementation.




-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1. Approach
- To fulfill the project objectives, a real-time Q&A generator system was developed using the following advanced technologies:
  - Gemini-Pro: A generative AI model that enhances response quality and contextual relevance.
  - LangChain: A framework for integrating language models that simplifies document processing and question answering.
  -  Google Generative AI Embeddings: Employed for efficient similarity searches through embedding text into dense vectors.


2. Technologies Used
LangChain: For building chains of actions and integrating multiple language models.
Generative AI: To generate natural language responses and content.
Google Gemini: A large language model providing generative capabilities.
LLMs (Large Language Models): For understanding and processing the text.
Transformers: For leveraging state-of-the-art NLP techniques.
3. Implementation Steps
- PDF Upload and Text Extraction: Users upload PDF documents, and text is extracted using the PyPDF2 library.
- Text Chunking: Extracted text is divided into manageable chunks to optimize processing for similarity searches.
- Creating FAISS Index: A FAISS index is created for fast retrieval of relevant information based on user queries.
- User Interaction: The application allows users to generate multiple-choice questions (MCQs) and ask questions about the PDF content.
- Q&A Generation: Tailored prompts guide the language model to generate accurate answers based on the extracted context.

4. User Interaction:
- The application features a user-friendly interface where users can:
- Generate Multiple Choice Questions (MCQs) based on specific topics.
- Ask questions about the PDF content for instant answers.

Q&A Generation:
The system uses a tailored prompt to guide the language model in generating accurate answers based on the context extracted from the uploaded PDF.

5. Output:
- Generated MCQs and answers to user questions are displayed in the application, allowing for immediate feedback and further interaction.


6. Conclusion
- This project effectively automates the generation of Q&A content, saving time for educators and enhancing the learning experience for students.
- By leveraging cutting-edge AI technologies, the system provides a scalable and efficient solution to address the challenges of manual Q&A creation.


## Deployment

To deploy this project run

```bash
  streamlit run filename.py
```


