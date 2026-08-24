FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install

# Copy source
COPY . .

# Build
RUN npm run build

# Production server
FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=0 /app/build ./build

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
