./llama-server \
	-hf unsloth/Qwen3-1.7B-GGUF:Q4_K_M \
	-t 4 \
	--no-mmap \
	-fit off \
	-fa on \
	--host 0.0.0.0 \
	--port 56810
