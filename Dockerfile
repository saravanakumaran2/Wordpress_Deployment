# Use the official WordPress image as the base
FROM wordpress:latest

# Copy your local WordPress code into the container
COPY . /var/www/html/

# Set the necessary environment variables for connecting to the database
ENV WORDPRESS_DB_HOST=your-database-host:3306
ENV WORDPRESS_DB_NAME=your-database-name
ENV WORDPRESS_DB_USER=your-database-username
ENV WORDPRESS_DB_PASSWORD=your-database-password

# Set proper permissions for the WordPress files
RUN chown -R www-data:www-data /var/www/html

# Expose the port that WordPress runs on
EXPOSE 80

# Start Apache in the foreground to serve the WordPress site
CMD ["apache2-foreground"]
