FROM php:8.0-apache
# Install dependencies required by WordPress
RUN apt-get update && apt-get install -y \
   libpng-dev \
   libjpeg-dev \
   libfreetype6-dev \
   libonig-dev \
   libzip-dev \
   zip \
   unzip \
&& docker-php-ext-configure gd --with-freetype --with-jpeg \
&& docker-php-ext-install gd \
&& docker-php-ext-install mysqli pdo pdo_mysql \
&& docker-php-ext-enable mysqli
# Enable Apache rewrite module
RUN a2enmod rewrite
# Set working directory inside the container
WORKDIR /var/www/html
# Copy WordPress files into the container
COPY . /var/www/html
# Set proper permissions for WordPress
RUN chown -R www-data:www-data /var/www/html && \
   chmod -R 755 /var/www/html
# Expose the default HTTP port
EXPOSE 80
# Start Apache
CMD ["apache2-foreground"]
