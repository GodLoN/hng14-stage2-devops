# Stage 1: Build
FROM node:18-slim as builder
WORKDIR /app
COPY package*.json ./
RUN npm install --production

# Stage 2: Production
FROM node:18-slim
WORKDIR /app

# Create non-root user
RUN useradd -m frontenduser
USER frontenduser

# Copy from builder
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Requirement: Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000', (r) => {if(r.statusCode !== 200) process.exit(1)})" || exit 1

EXPOSE 3000
CMD ["node", "app.js"]
