# rag-math-tutor
---

## Environment Variables

Create a `.env` file in the root directory with the following content, or modify as needed:

```
# Shared Environment Variables
OPENAI_API_KEY=your_api_key

```

---

## Build and Start the App

Follow these steps to build and run the application:

1. **Clone the Repository**:
   If you haven't already, clone the repository to your local machine.

   ```bash
   git clone https://github.com/rag-math-tutor.git
   cd rag-math-tutor
   ```

2. **Build and Start the Services**:
   Use `docker-compose` to build and start the services.

   ```bash
   docker-compose up --build
   ```

3. **Access the Services**:
   - **UI**: Open your browser and navigate to [http://localhost:8501](http://localhost:8501).
   - **API**: Access the chatbot API at [http://localhost:8000](http://localhost:8000).

---

## Stopping the Services

To stop the running services, use:

```bash
docker-compose down
```

This will stop and remove the containers but preserve the images.

---

Happy coding! 🚀
