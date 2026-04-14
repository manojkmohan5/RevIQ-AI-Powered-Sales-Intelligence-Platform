"use client";

import React, { useState, useEffect, useRef } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Send, Bot, User, BarChart3, TrendingUp, Users } from 'lucide-react';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [messages, setMessages] = useState<{role: string, content: string, sql?: string, data?: any[]}[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/dashboard')
      .then(res => res.json())
      .then(data => setDashboardData(data))
      .catch(err => console.error("Could not load dashboard data. Ensure backend is running.", err));
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = inputValue;
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setInputValue('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMessage })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: data.answer,
        sql: data.sql,
        data: data.data
      }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', content: "Sorry, I encountered an error. Ensure the fast api backend is running." }]);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (val: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(val || 0);

  return (
    <div className="min-h-screen bg-[var(--background)] text-[var(--foreground)] p-6 font-sans">
      <header className="flex items-center justify-between mb-8 pb-4 border-b border-[var(--panel-border)]">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
            Nexus Intelligence
          </h1>
          <p className="text-gray-400 mt-1">End-to-End Sales Analytics Pipeline</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="h-2 w-2 rounded-full bg-[var(--success)] shadow-[0_0_8px_var(--success)] animate-pulse"></div>
          <span className="text-sm text-gray-300">Live Connection: DuckDB Warehouse</span>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Main Dashboard Section */}
        <div className="lg:col-span-2 space-y-6">
          <div className="grid grid-cols-3 gap-4">
            <div className="glass-panel p-5 metric-card">
              <div className="flex items-center gap-3 mb-2 text-gray-300">
                <TrendingUp size={18} className="text-blue-400" />
                <h3 className="font-medium">Total Pipeline Rev</h3>
              </div>
              <p className="text-3xl font-semibold tracking-tight">
                {dashboardData ? formatCurrency(dashboardData.total_revenue) : 'Loading...'}
              </p>
            </div>
            
            <div className="glass-panel p-5 metric-card">
              <div className="flex items-center gap-3 mb-2 text-gray-300">
                <BarChart3 size={18} className="text-emerald-400" />
                <h3 className="font-medium">Win Rate Base</h3>
              </div>
              <p className="text-3xl font-semibold tracking-tight">
                24.5%
              </p>
            </div>
            
            <div className="glass-panel p-5 metric-card">
              <div className="flex items-center gap-3 mb-2 text-gray-300">
                <Users size={18} className="text-purple-400" />
                <h3 className="font-medium">Total Reps</h3>
              </div>
              <p className="text-3xl font-semibold tracking-tight">
                {dashboardData ? dashboardData.top_reps.length : '-'}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div className="glass-panel p-5 h-[350px]">
              <h3 className="font-medium mb-4">Revenue by Region</h3>
              {dashboardData && (
                <ResponsiveContainer width="100%" height="85%">
                  <PieChart>
                    <Pie
                      data={dashboardData.sales_by_region}
                      dataKey="amount"
                      nameKey="region"
                      cx="50%" cy="50%" innerRadius={60} outerRadius={100}
                      paddingAngle={5}
                    >
                      {dashboardData.sales_by_region.map((entry: any, index: number) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(val: any) => formatCurrency(val as number)}
                      contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              )}
            </div>

            <div className="glass-panel p-5 h-[350px]">
              <h3 className="font-medium mb-4">Top Performing Reps</h3>
              {dashboardData && (
                <ResponsiveContainer width="100%" height="85%">
                  <BarChart data={dashboardData.top_reps} layout="vertical" margin={{ left: 30 }}>
                    <XAxis type="number" hide />
                    <YAxis dataKey="rep" type="category" axisLine={false} tickLine={false} tick={{fill: '#94a3b8'}} />
                    <Tooltip 
                      formatter={(val: any) => formatCurrency(val as number)}
                      cursor={{fill: 'rgba(255,255,255,0.05)'}}
                      contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                    />
                    <Bar dataKey="won_amount" fill="var(--accent)" radius={[0, 4, 4, 0]} barSize={20} />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>
        </div>

        {/* AI Chat Interface */}
        <div className="glass-panel flex flex-col h-[650px] lg:col-span-1">
          <div className="p-4 border-b border-[var(--panel-border)] bg-[rgba(0,0,0,0.2)] rounded-t-2xl">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-500/20 text-blue-400 rounded-lg">
                <Bot size={20} />
              </div>
              <div>
                <h3 className="font-medium text-white">Ask your Data</h3>
                <p className="text-xs text-gray-400">Powered by Ollama (phi3) & Langchain</p>
              </div>
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 ? (
              <div className="text-center text-gray-400 mt-10">
                <Bot size={40} className="mx-auto mb-3 opacity-50" />
                <p>Ask anything about your CRM data in plain English!</p>
                <div className="mt-4 flex flex-col gap-2">
                  <button onClick={() => setInputValue("What is our total revenue?")} className="text-sm bg-white/5 hover:bg-white/10 p-2 rounded border border-white/10 transition">"What is our total revenue?"</button>
                  <button onClick={() => setInputValue("Who is the best sales rep by won amount?")} className="text-sm bg-white/5 hover:bg-white/10 p-2 rounded border border-white/10 transition">"Who is the best sales rep?"</button>
                </div>
              </div>
            ) : (
              messages.map((msg, i) => (
                <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[85%] p-3 text-sm ${msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-ai'}`}>
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                    
                    {/* Render SQL if available */}
                    {msg.sql && (
                      <div className="mt-3 p-2 bg-black/40 rounded border border-white/10 font-mono text-[10px] text-gray-400 overflow-x-auto">
                        <span className="text-emerald-500 block mb-1">// SQL Executed</span>
                        {msg.sql}
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
            {loading && (
              <div className="flex justify-start">
                <div className="chat-bubble-ai p-3 text-sm flex items-center gap-2">
                  <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                  <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
          
          <div className="p-4 border-t border-[var(--panel-border)]">
            <form onSubmit={handleSendMessage} className="relative">
              <input 
                type="text" 
                value={inputValue}
                onChange={e => setInputValue(e.target.value)}
                placeholder="Ask about your sales metrics..." 
                className="w-full bg-black/30 border border-[var(--panel-border)] rounded-full py-3 pl-4 pr-12 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all text-white placeholder-gray-500"
              />
              <button 
                type="submit" 
                disabled={loading}
                className="absolute right-2 top-2 p-1.5 bg-blue-600 hover:bg-blue-500 rounded-full text-white transition-colors disabled:opacity-50"
              >
                <Send size={16} />
              </button>
            </form>
          </div>
        </div>

      </div>
    </div>
  );
}
