from django.db import models


class Customer(models.Model):
    CABLE_SERVICE = 'C'
    INTERNET_SERVICE = 'I'
    CABLE_INTERNET_SERVICE = 'A'
    MEMBERSHIP_CHOICES = [
        (CABLE_SERVICE, 'Cable'),
        (INTERNET_SERVICE, 'Internet'),
        (CABLE_INTERNET_SERVICE, 'Cable + Internet')
    ]
    PENDING = 'P'
    INSTALLED = 'I'
    CANCELLED = 'C'
    INSTALLATION_CHOICES = [
        (PENDING, 'Pendiente'),
        (INSTALLED, 'Instalado'),
        (CANCELLED, 'Cancelado')
    ]

    names = models.CharField(max_length=255, verbose_name='Nombres')
    last_names = models.CharField(max_length=255, verbose_name='Apellidos')
    dni = models.CharField(max_length=255, unique=True, verbose_name='Cédula')
    email = models.EmailField(max_length=255, verbose_name='Correo electrónico')
    phone = models.CharField(max_length=255, verbose_name='Teléfono')
    price_contract = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monto de instalación')
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=CABLE_SERVICE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    status_installation = models.CharField(max_length=1, choices=INSTALLATION_CHOICES, default=PENDING)
    date_installation = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de instalación')
    active = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return f"{self.names} {self.last_names}"


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sector = models.CharField(max_length=255, verbose_name='Sector')
    principal_street = models.CharField(max_length=255, verbose_name='Calle principal')
    secondary_street = models.CharField(max_length=255, verbose_name='Calle secundaria')

    def __str__(self):
        return f"{self.principal_street} y {self.secondary_street}"


class MontlyPayment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    invoice = models.CharField(max_length=255, verbose_name='Factura')
    amount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monto')
    date = models.DateField(verbose_name='Fecha')

    def __str__(self):
        return f"{self.customer.names} {self.customer.last_names}"

    @property
    def initial_payment_at(self):
        if self.customer.status_installation == 'I':
            return self.customer.date_installation


class WorkOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    number_of_order = models.CharField(max_length=255, verbose_name='Número de orden')
    date = models.DateField(verbose_name='Fecha')
    description = models.TextField(verbose_name='Descripción')


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Precio')
    inventory = models.IntegerField(verbose_name='Stock')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    last_update = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return self.title


class InstallationMaterials(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    material = models.CharField(max_length=255, verbose_name='Material')
    quantity = models.IntegerField(verbose_name='Cantidad')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Precio')
