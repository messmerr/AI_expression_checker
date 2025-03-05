#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
表达式等价比对器GUI版本
提供图形界面来判断两个数学表达式是否等价，通过调用大模型API进行判断
复用命令行版本的核心功能，展示程序的可扩展性
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import threading
import sys
import json

# 导入命令行版本的核心功能
from expression_equivalence import generate_prompt, call_llm_api, parse_equivalence_result

class ExpressionEquivalenceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("表达式等价比对器")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # 从环境变量获取默认值
        self.default_base_url = os.environ.get('LLM_API_BASE_URL', 'https://api.openai.com/v1')
        self.default_api_key = os.environ.get('LLM_API_KEY', '')
        self.default_model = os.environ.get('LLM_MODEL', 'gpt-3.5-turbo')
        
        self.create_widgets()
        self.center_window()
    
    def center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def create_widgets(self):
        """创建GUI组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 表达式输入区域
        expr_frame = ttk.LabelFrame(main_frame, text="表达式输入", padding="10")
        expr_frame.pack(fill=tk.X, pady=5)
        
        # 第一个表达式
        ttk.Label(expr_frame, text="表达式1:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.expr1_entry = ttk.Entry(expr_frame, width=50)
        self.expr1_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5, padx=5)
        
        # 第二个表达式
        ttk.Label(expr_frame, text="表达式2:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.expr2_entry = ttk.Entry(expr_frame, width=50)
        self.expr2_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5, padx=5)
        
        # API设置区域
        api_frame = ttk.LabelFrame(main_frame, text="API设置", padding="10")
        api_frame.pack(fill=tk.X, pady=5)
        
        # Base URL
        ttk.Label(api_frame, text="Base URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.base_url_entry = ttk.Entry(api_frame, width=50)
        self.base_url_entry.insert(0, self.default_base_url)
        self.base_url_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5, padx=5)
        
        # API Key
        ttk.Label(api_frame, text="API Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.api_key_entry = ttk.Entry(api_frame, width=50, show="*")
        self.api_key_entry.insert(0, self.default_api_key)
        self.api_key_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5, padx=5)
        
        # 显示/隐藏API Key按钮
        self.show_key = tk.BooleanVar(value=False)
        self.show_key_check = ttk.Checkbutton(
            api_frame, 
            text="显示API Key", 
            variable=self.show_key,
            command=self.toggle_api_key_visibility
        )
        self.show_key_check.grid(row=1, column=2, padx=5)
        
        # 模型名称
        ttk.Label(api_frame, text="模型名称:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.model_entry = ttk.Entry(api_frame, width=50)
        self.model_entry.insert(0, self.default_model)
        self.model_entry.grid(row=2, column=1, sticky=tk.W+tk.E, pady=5, padx=5)
        
        # 温度参数
        ttk.Label(api_frame, text="温度参数:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.temperature_var = tk.DoubleVar(value=0.0)
        self.temperature_scale = ttk.Scale(
            api_frame, 
            from_=0.0, 
            to=1.0, 
            orient=tk.HORIZONTAL,
            variable=self.temperature_var,
            length=200
        )
        self.temperature_scale.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        self.temperature_label = ttk.Label(api_frame, text="0.0")
        self.temperature_label.grid(row=3, column=1, sticky=tk.E, pady=5, padx=5)
        self.temperature_scale.bind("<Motion>", self.update_temperature_label)
        
        # 详细模式选项
        self.verbose_var = tk.BooleanVar(value=False)
        self.verbose_check = ttk.Checkbutton(
            api_frame, 
            text="详细模式", 
            variable=self.verbose_var
        )
        self.verbose_check.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # 判断按钮
        self.check_button = ttk.Button(
            button_frame, 
            text="判断等价性", 
            command=self.check_equivalence
        )
        self.check_button.pack(side=tk.LEFT, padx=5)
        
        # 清除按钮
        self.clear_button = ttk.Button(
            button_frame, 
            text="清除输入", 
            command=self.clear_inputs
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="判断结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=10)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        self.status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def toggle_api_key_visibility(self):
        """切换API Key的可见性"""
        if self.show_key.get():
            self.api_key_entry.config(show="")
        else:
            self.api_key_entry.config(show="*")
    
    def update_temperature_label(self, event=None):
        """更新温度参数标签"""
        self.temperature_label.config(text=f"{self.temperature_var.get():.1f}")
    
    def clear_inputs(self):
        """清除输入框内容"""
        self.expr1_entry.delete(0, tk.END)
        self.expr2_entry.delete(0, tk.END)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.status_var.set("已清除输入")
    
    def append_to_result(self, text):
        """向结果文本框添加文本"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)
    
    def check_equivalence(self):
        """检查表达式等价性"""
        # 获取输入
        expr1 = self.expr1_entry.get().strip()
        expr2 = self.expr2_entry.get().strip()
        
        # 验证输入
        if not expr1 or not expr2:
            messagebox.showerror("输入错误", "请输入两个表达式")
            return
        
        base_url = self.base_url_entry.get().strip()
        api_key = self.api_key_entry.get().strip()
        model = self.model_entry.get().strip()
        temperature = self.temperature_var.get()
        verbose = self.verbose_var.get()
        
        if not base_url or not api_key or not model:
            messagebox.showerror("输入错误", "请填写API设置")
            return
        
        # 清除之前的结果
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        
        # 禁用按钮，防止重复点击
        self.check_button.config(state=tk.DISABLED)
        self.status_var.set("正在判断中...")
        
        # 在新线程中执行API调用，避免界面卡顿
        threading.Thread(
            target=self.perform_equivalence_check,
            args=(expr1, expr2, base_url, api_key, model, temperature, verbose),
            daemon=True
        ).start()
    
    def perform_equivalence_check(self, expr1, expr2, base_url, api_key, model, temperature, verbose):
        """执行等价性检查（在单独线程中运行）"""
        try:
            # 使用命令行版本的函数生成提示
            messages = generate_prompt(expr1, expr2)
            
            if verbose:
                self.append_to_result("生成的提示:")
                for msg in messages:
                    self.append_to_result(f"{msg['role']}: {msg['content']}")
                self.append_to_result("")
            
            self.append_to_result("正在调用API判断表达式是否等价...")
            
            # 使用命令行版本的函数调用API
            response_text = call_llm_api(base_url, api_key, model, messages, temperature)
            
            if verbose:
                self.append_to_result(f"API原始响应: {response_text}")
                self.append_to_result("")
            
            # 使用命令行版本的函数解析结果
            is_equivalent, raw_response = parse_equivalence_result(response_text)
            
            # 显示结果
            self.append_to_result("判断结果:")
            self.append_to_result(f"表达式1: {expr1}")
            self.append_to_result(f"表达式2: {expr2}")
            
            if is_equivalent is True:
                self.append_to_result("结论: 等价 ✓")
                self.status_var.set("判断完成: 等价")
            elif is_equivalent is False:
                self.append_to_result("结论: 不等价 ✗")
                self.status_var.set("判断完成: 不等价")
            else:
                self.append_to_result(f"结论: 无法确定 (?)")
                self.append_to_result(f"原始响应: {raw_response}")
                self.append_to_result("提示: API返回的内容不包含明确的'等价'或'不等价'关键词")
                self.status_var.set("判断完成: 无法确定")
            
        except Exception as e:
            self.append_to_result(f"错误: {str(e)}")
            self.status_var.set(f"发生错误: {str(e)}")
        
        finally:
            # 重新启用按钮
            self.root.after(0, lambda: self.check_button.config(state=tk.NORMAL))

def main():
    """主函数"""
    root = tk.Tk()
    app = ExpressionEquivalenceGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 