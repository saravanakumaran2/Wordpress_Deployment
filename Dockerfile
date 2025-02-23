# Use Apache as the base image
FROM php:8.0-apache
# Use Apache as the base image
# Install PHP extensions required for WordPress
RUN apt-get update && apt-get install -y \
   libpng-dev \
   libjpeg-dev \
   libfreetype6-dev \
   libzip-dev \
   zip \
   unzip \
&& docker-php-ext-configure gd --with-freetype --with-jpeg \
&& docker-php-ext-install gd mysqli pdo pdo_mysql \
&& docker-php-ext-enable mysqli

# Enable Apache rewrite module
RUN a2enmod rewrite

# Add ServerName directive to avoid the "Could not reliably determine the server's fully qualified domain name" warning
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Set working directory inside the container
WORKDIR /var/www/html

# Copy local WordPress files to the container
COPY . /var/www/html

# Copy custom wp-config.php to replace the default one
COPY wp-config.php /var/www/html/wp-config.php

# Set environment variables for MySQL credentials
ENV WORDPRESS_DB_HOST=db:3306
ENV WORDPRESS_DB_NAME=wordpress
ENV WORDPRESS_DB_USER=wordpress
ENV WORDPRESS_DB_PASSWORD=wordpress

# Set proper permissions for WordPress files
RUN chown -R www-data:www-data /var/www/html && chmod -R 755 /var/www/html

# Expose the Apache port
EXPOSE 80

# Start Apache in the foreground
CMD ["apache2-foreground"]
