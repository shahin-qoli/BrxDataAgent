from django.db import models

# Create your models here.
class Vendor(models.Model):
    bpcode = models.CharField(max_length=200, blank=True, null=True)
    bpname = models.CharField(max_length=200, blank=True, null=True)
    bpcreatedate = models.DateField(max_length=200, blank=True, null=True)


class Ocrd(models.Model):
    bpcode = models.CharField(max_length=200, blank=True, null=True)
    bpname = models.CharField(max_length=200, blank=True, null=True)
    bpcreatedate = models.DateField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.bpcode

class Oslp(models.Model):
    slpcode = models.IntegerField()
    slpname = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.slpname


class Ordr(models.Model):
    bpcode = models.CharField(max_length=200)
    ocrd = models.ForeignKey(Ocrd, on_delete=models.CASCADE)
    slpcode = models.IntegerField()
    oslp = models.ForeignKey(Oslp, on_delete=models.CASCADE)
    docdate = models.DateField()

##table for CC, rule2 and rule 3
class VwAgentPurchaseFrequencyCClub(models.Model):
    bpcode = models.CharField(max_length=200)
    ocrd = models.ForeignKey(Ocrd, on_delete=models.CASCADE)
    quarternum = models.IntegerField()
    year = models.IntegerField()
    totalprice = models.DecimalField()
    countinvoice = models.IntegerField()
    countinvoice7Mtoup = models.IntegerField()
    countinvoicebetween5to7M = models.IntegerField()

    def __str__(self):
        return self.cardcode


##table for CC, rule1
class VwAgentSKUCustomerClub(models.Model):
    bpcode = models.CharField(max_length=200)
    ocrd = models.ForeignKey(Ocrd, on_delete=models.CASCADE)
    quarternum = models.IntegerField()
    year = models.IntegerField()
    totalprice = models.DecimalField()
    countofsku = models.IntegerField()
    countofsku500k = models.IntegerField()


    def __str__(self):
        return self.cardcode

class Vwvisitorsku(models.Model):
    slpcode = models.IntegerField()
    oslp = models.ForeignKey(Oslp, on_delete=models.CASCADE)
    jmonthn = models.IntegerField()
    jyear = models.IntegerField()
    countuniquesku = models.IntegerField()
    countuniquecustomer = models.IntegerField(default=0)
    def __int__(self):
       return self.slpcode


class Vwcustomerclub(models.Model):
     bpcode = models.CharField(max_length=200)
     quarter = models.CharField(max_length=200)
     year = models.CharField(max_length=200)
     numberofinovices = models.IntegerField(blank=True, null=True)
     countsku = models.IntegerField(blank=True, null=True)
     countskuup500kT = models.IntegerField(blank=True, null=True)
     totalprice = models.DecimalField(max_digits=200,decimal_places=0, blank=True, null=True)
     ocrd = models.ForeignKey(Ocrd,on_delete=models.CASCADE,default=0)

     def __str__(self):
         return self.bpcode


class VwagentActiveCustomerPerVisitor(models.Model):
    slpcode = models.IntegerField()
    oslp = models.ForeignKey(Oslp, on_delete=models.CASCADE)
    quartern = models.IntegerField()
    activecustomer = models.IntegerField()

    def __int__(self):
        return self.slpcode


class NewCustomer(models.Model):
    bpcode = models.CharField(max_length=200, blank=True, null=True)
    bpcreatedate = models.DateField(max_length=200, blank=True, null=True)
    bpused = models.BooleanField(default=True)
    bpuseddate = models.DateField(max_length=200, blank=True, null=True)
    slpcodeused = models.CharField(max_length=200, blank=True, null= True)
    oslp = models.ForeignKey(Oslp, on_delete=models.CASCADE,blank=True, null=True)
    ocrd = models.ForeignKey(Ocrd,on_delete=models.CASCADE,default=0)
    def __str__(self):
        return self.bpcode

class OcrdOslp(models.Model):
    ocrd = models.ForeignKey(Ocrd,on_delete=models.CASCADE)
    bpcode = models.CharField(max_length=200)
    slpcode = models.IntegerField(blank=True, null=True)
    oslp = models.ForeignKey(Oslp,on_delete=models.CASCADE,blank=True, null=True)
    def __str__(self):
        return self.bpcode


class Rules(models.Model):
    key = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return self.key


"""class RuleParameters(models.Model):
    key = models.CharField(max_length=200)
    value = models.IntegerField()
    ruleid = models.CharField(max_length=200)
    id = models.IntegerField()
    deleted = models.BooleanField(default=False)
    isdeleted = models.BooleanField(default=False)
    Code = models.CharField(max_length=200)
    rules = models.ForeignKey(Rules, on_delete=models.CASCADE)

    def __str__(self):
        return self.key


"""
