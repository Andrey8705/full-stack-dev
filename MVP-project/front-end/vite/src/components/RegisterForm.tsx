
import React, { useState } from 'react';
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

const RegisterForm = () => {
  const [name, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      name,
      email,
      password,
    };

    try {
      const response = await fetch("http://localhost:8000/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
    
      const data = await response.json();
      if (response.ok) {
        alert("User created successfully");
      } else {
        alert(`Error: ${data.message || "unknown error"}`);
      }
    } catch (error) {
      console.error("An unexpected error occurred:", error);
    }
  };

  return (
    <Card className="rounded-xl border bg-[#00000096] text-[#ffe4c4] shadow">
      <CardHeader>
        <CardTitle className="text-2xl">Create an Account</CardTitle>
        <CardDescription>Enter your details below to create a new account</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit}>
          <div className="flex flex-col gap-6">
                {/* Username Field */}
            <Label htmlFor="username">Username</Label>
            <Input
              id="username"
              type="text"
              placeholder="Enter your username"
              value={name}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

              {/* Email Field */}
          <div className="grid gap-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

              {/* Password Field */}
          <div className="grid gap-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password" 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required 
              />
          </div>

              {/* Submit Button */}
          <Button type="submit" className="w-full">
            Register
          </Button>
          <div className="mt-4 text-center text-sm">
            Already have an account?{" "}
              <a href="#" className="underline underline-offset-4">
                Log in
              </a>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

export default RegisterForm;
