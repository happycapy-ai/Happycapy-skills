# HappyCapy Environment Constraints

## System Configuration

- **OS**: Linux 6.12.27-fly (Debian-based, Fly.io)
- **Architecture**: x86_64
- **User**: node (uid=1000)
- **Shell**: /usr/bin/zsh

## Hardware Resources

- **CPU**: AMD EPYC, 2 cores
- **Memory**: ~4GB total, ~3GB available for use
- **Disk**: 8GB total, ~7GB available

## Available Runtimes

### ✅ Available

- **Python**: 3.11.2
- **Node.js**: 24.13.0
- **NPM**: 11.6.2
- **Git**: 2.39.5

### ❌ NOT Available

- Docker
- Java
- Ruby
- Go

## Preinstalled Tools

### Document Processing
- `pandoc` - Universal document converter
- `ghostscript` - PDF processing

### Image Processing
- `convert` (ImageMagick) - Image manipulation
- `identify` (ImageMagick) - Image information

### Data Processing
- `jq` - JSON processor

### Development
- `make` - Build automation
- `gcc`, `g++` - C/C++ compilers

### Utilities
- `curl`, `wget` - HTTP clients
- `unzip`, `tar` - Archive tools

## Environment Variables

### Available API Keys
- `AI_GATEWAY_API_KEY` - For AI services
- `ANTHROPIC_API_KEY` - For Claude API
- `CAPY_USER_EMAIL` - User email
- `CAPY_USER_EMAIL_ALIAS` - Email alias

## Network

- ✅ External access available
- ⚠️  Port 3001 reserved (don't use)
- ✅ Other ports available for services

## Skill Development Constraints

### Memory
- ⚠️  Limit: 4GB total
- 💡 Best practice: Design for < 2GB usage
- ❌ Avoid: Loading large files entirely into memory
- ✅ Use: Streaming, chunked processing

### CPU
- ⚠️  Limit: 2 cores
- ❌ Avoid: Heavy parallel processing
- ✅ Use: Sequential processing, reasonable concurrency

### Dependencies
- ✅ Python packages via `pip`
- ✅ Node packages via `npm`
- ❌ No system packages requiring `sudo`
- ❌ No Docker images

### Best Practices

1. **Use preinstalled tools**
   - pandoc for document conversion
   - ImageMagick for image processing
   - jq for JSON processing

2. **Keep dependencies minimal**
   - < 10 core dependencies ideal
   - Avoid large ML frameworks (TensorFlow, PyTorch)

3. **Memory efficiency**
   - Stream large files
   - Process in chunks
   - Clean up temp files

4. **Native execution**
   - No Docker, no containers
   - Direct Python/Node.js execution
   - Use subprocess for CLI tools

## Example: Good vs Bad

### ❌ Bad: Memory-intensive
```python
# Loads entire 1GB file into memory
data = open('large_file.csv').read()
process(data)
```

### ✅ Good: Streaming
```python
# Processes line by line
with open('large_file.csv') as f:
    for line in f:
        process(line)
```

### ❌ Bad: Docker dependency
```python
subprocess.run(['docker', 'run', 'image', 'command'])
```

### ✅ Good: Native execution
```python
subprocess.run(['python', 'script.py'])
```

### ❌ Bad: Unavailable runtime
```python
subprocess.run(['java', '-jar', 'tool.jar'])
```

### ✅ Good: Available runtime
```python
subprocess.run(['pandoc', 'input.md', '-o', 'output.pdf'])
```
