# Use an official Node.js runtime as the base image
FROM node:14

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application files to the container
COPY . .

# Build the React application
RUN npm run build

# Set the production-ready server to serve the built React app
CMD ["npx", "serve", "-s", "build", "-l", "3000"]

# Expose the port the application will run on
EXPOSE 3000
