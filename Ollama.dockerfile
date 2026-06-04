FROM ollama/ollama:latest

COPY ollama-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV OLLAMA_LOG_LEVEL=warn

ENTRYPOINT ["/entrypoint.sh"]
    