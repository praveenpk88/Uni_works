package org.example;

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class Main {
    public static void main(String args[]){
        Account a1 = new Account("Tan A K", "S123", 24.5);
        Account a2 = new Account("Smith T", "S124", 1200.0);
        a1.deposit(100);
        a1.withdraw(2000);
        a2.deposit(120);
        a2.withdraw(80);
        System.out.println("Balance for " + a1.getName() + " is " + a1.getBalance());
        System.out.println("Balance for " + a2.getName() + " is " + a2.getBalance());
    }
}

class Account{
    private String name;
    private String ID;
    private double balance;
    public Account(String name, String ID, double balance){
        this.name = name;
        this.ID = ID;
        this.balance = balance;
    }
    public double getBalance(){
        return balance;
    }
    public boolean withdraw(double amt){
        if (amt > 0 && amt <= balance){
            balance -= amt;
            return true;
        }
        return false;
    }
    public void deposit(double amt){
        if (amt > 0){
            balance += amt;
        }
    }
    public String getName(){
        return name;
    }
    public void addInterest(double rate){
        balance += balance * rate / 100;
    }
}