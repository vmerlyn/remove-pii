# Use ocrmypdf's official Docker image which includes all dependencies
FROM jbarlow83/ocrmypdf:latest

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy application code
COPY main.py ./

# Set Python path
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "main.py"]