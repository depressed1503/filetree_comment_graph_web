FROM python:3.11-slim

RUN apt-get update && apt-get install -y git
WORKDIR /app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN git clone --depth 1 https://github.com/depressed1503/filetree_comment_graph.git
RUN pip install --no-cache-dir -r filetree_comment_graph/requirements.txt
WORKDIR /app/filetree_comment_graph
RUN python3 -m build
RUN pip install dist/filetree_comment_graph-*.whl --force-reinstall
WORKDIR /app
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]