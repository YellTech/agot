import customtkinter as ctk
import sys
from tkinter import messagebox
from model.db_access import DbAccess
import bcrypt
import random, string


class App(ctk.CTk):
    def __init__(self, user):
        super().__init__()

        self.list_entries = []
        self.show_password = False
        self.user = user
        self.login_success = False
        self.flag_login = 0
        
        # Configuração da janela
        self.geometry("1280x720")  # Tamanho inicial da janela
        self.title("AGOT")

        # Configurando a grade para permitir expansão proporcional
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Criando o side menu à esquerda
        self.side_menu = ctk.CTkFrame(self, width=200, border_width=1)
        self.side_menu.grid(row=0, column=0, sticky="nsw")

        self.menu_title = ctk.CTkLabel(self.side_menu, text="MENU", font=("TkDefaultFont", 16, "bold"))
        self.menu_title.pack(pady=10, padx=10, fill="x")
        
        # Exemplo de botões no side menu
        self.bt_home = ctk.CTkButton(self.side_menu, text="INICIO", command=self.show_bt_home, font=("TkDefaultFont", 14))
        self.bt_home.pack(pady=10, padx=10, fill="x")
        
        self.bt_user = ctk.CTkButton(self.side_menu, text="USUÁRIO", command=self.show_bt_users, font=("TkDefaultFont", 14))
        self.bt_user.pack(pady=10, padx=10, fill="x")

        self.bt_clients = ctk.CTkButton(self.side_menu, text="CLIENTES", command=self.show_clients, font=("TkDefaultFont", 14))
        self.bt_clients.pack(pady=10, padx=10, fill="x")
        
        self.bt_debts = ctk.CTkButton(self.side_menu, text="DIVIDAS", command=self.show_debts, font=("TkDefaultFont", 14))
        self.bt_debts.pack(pady=10, padx=10, fill="x")
        
        self.bt_dash = ctk.CTkButton(self.side_menu, text="DASHBOARDS", command=self.show_dashboards, font=("TkDefaultFont", 14))
        self.bt_dash.pack(pady=10, padx=10, fill="x")
        
        self.bt_logout = ctk.CTkButton(self.side_menu, text="SAIR", command=self.logout, font=("TkDefaultFont", 14))
        self.bt_logout.pack(pady=10, padx=10, fill="x")

        # Criando a área de exibição de conteúdo
        self.content_area = ctk.CTkFrame(self, border_width=1)
        self.content_area.grid(row=0, column=1, sticky="nsew")

        if self.user:
            self.show_login()
        else:
            self.show_create_user()
        
    def show_login(self):
        self.clear_content_area()
        # Adicionando elementos no content area
        self.label = ctk.CTkLabel(self.content_area, text="Insira suas credênciais para acessar o sistema.", 
                                  font=("TkDefaultFont", 14, "bold"))
        self.label.pack(pady=(30, 0), padx=20)
        
        self.entry_login_user = ctk.CTkEntry(self.content_area, placeholder_text="Usuário", width=200, height=35, 
                                          font=("TkDefaultFont", 14))
        self.entry_login_user.pack(pady=20, padx=20)
        
        self.entry_login_password = ctk.CTkEntry(self.content_area, placeholder_text="Senha", show="*", width=200, height=35,
                                           font=("TkDefaultFont", 14))
        self.entry_login_password.pack(pady=(0, 0), padx=20)
        self.entry_login_password.bind("<Return>", lambda event: self.valid_login())

        self.label_recovery = ctk.CTkLabel(self.content_area, text="Esqueceu sua senha?", font=("TkDefaultFont", 10, "bold"),
                                           cursor="hand2")
        self.label_recovery.pack(pady=(0, 10), padx=20)
        self.label_recovery.bind("<Button-1>", lambda event: self.show_recovery())
        self.label_recovery.bind("<Enter>", lambda event: self.label_recovery.configure(text_color="red"))
        self.label_recovery.bind("<Leave>", lambda event: self.label_recovery.configure(text_color="white"))
        
        self.login_button = ctk.CTkButton(self.content_area, text="ENTRAR", command= self.valid_login, height=35, 
                                          font=("TkDefaultFont", 14))
        self.login_button.pack(pady=20, padx=20)
        
        if self.flag_login > 0:
            self.error_label = ctk.CTkLabel(self.content_area, 
                                                text=f"Usuário ou senha inválidos!\nTentativas restantes: {4 - self.flag_login}",
                                                text_color="red", font=("TkDefaultFont", 14))
            self.error_label.pack(pady=10, padx=20)
        
    def show_bt_home(self):
        if self.login_success:
            self.clear_content_area()
            self.label = ctk.CTkLabel(self.content_area, text="Conteúdo de Home")
            self.label.pack(pady=20, padx=20)

    def show_bt_users(self):
        if self.login_success:
            self.clear_content_area()
            self.label = ctk.CTkLabel(self.content_area, text="Conteúdo de Usuários")
            self.label.pack(pady=20, padx=20)

    def show_clients(self):
        if self.login_success:
            self.clear_content_area()
            self.label = ctk.CTkLabel(self.content_area, text="Conteúdo de Clientes")
            self.label.pack(pady=20, padx=20)
               
    def show_debts(self):
        if self.login_success:
            self.clear_content_area()
            self.label = ctk.CTkLabel(self.content_area, text="Conteúdo de Dividas")
            self.label.pack(pady=20, padx=20)
        
    def show_dashboards(self):
        if self.login_success:
            self.clear_content_area()
            self.label = ctk.CTkLabel(self.content_area, text="Conteúdo de Dashboards")
            self.label.pack(pady=20, padx=20)
            
    def show_recovery(self):
        self.clear_content_area()
        self.label = ctk.CTkLabel(self.content_area, text="Insira seu usuário")
        self.label.pack(pady=(20, 0), padx=20)
        self.rec_user = ctk.CTkEntry(self.content_area, placeholder_text="Insira seu usuário.", width=200)
        self.rec_user.pack(pady=20, padx=20)
        self.bt_check = ctk.CTkButton(self.content_area, text="VERIFICAR", command=lambda: self.rec_password(1))
        self.bt_check.pack(pady=20, padx=20)
        self.rec_question = ctk.CTkLabel(self.content_area, text="", font=("TkDefaultFont", 14, "bold"))
        
        self.rec_response = ctk.CTkEntry(self.content_area, placeholder_text="Digite a resposta secreta aqui.", width=300)
        
        self.bt_recovery = ctk.CTkButton(self.content_area, text="RECUPERAR", command=lambda: self.rec_password(2))
        
        self.voltar = ctk.CTkButton(self.content_area, text="VOLTAR", command= self.show_login, font=("TkDefaultFont", 14))
        self.voltar.pack(pady=20, padx=20)
    
    def show_create_user(self):
        self.clear_content_area()
        self.label = ctk.CTkLabel(self.content_area, text="Crie um usuário para poder utilizar o AGOT.",
                                  font=("TkDefaultFont", 14, "bold"))
        self.label.pack(pady=20, padx=20)
            
        self.cad_user = ctk.CTkEntry(self.content_area, placeholder_text="Usuário", width=200, height=35, 
                                          font=("TkDefaultFont", 14))
        self.cad_user.pack(pady=20, padx=20)
        
        self.cad_password = ctk.CTkEntry(self.content_area, placeholder_text="Senha", width=200, height=35, 
                                          font=("TkDefaultFont", 14))
        self.cad_password.pack(pady=20, padx=20)
        
        #self.toogle_cad = ctk.CTkSwitch(self.content_area, text="Ver senha?", command=lambda:self.toggle_password(self.cad_password))
        #self.toogle_cad.pack(pady=20, padx=20)
        
        self.cad_question = ctk.CTkEntry(self.content_area, placeholder_text="Pergunta secreta", width=300, height=35, 
                                          font=("TkDefaultFont", 14))
        self.cad_question.pack(pady=20, padx=20)
        
        self.cad_response = ctk.CTkEntry(self.content_area, placeholder_text="Resposta secreta", width=300, height=35, 
                                          font=("TkDefaultFont", 14))
        self.cad_response.pack(pady=20, padx=20)
        
        self.cad_button = ctk.CTkButton(self.content_area, text="CADASTRAR", command=self.create_user, font=("TkDefaultFont", 14, "bold"))
        self.cad_button.pack(pady=20, padx=20)
 
    def hash_creator(self, item):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(item.encode('utf-8'), salt)
        return hashed
    
    def check_hashed(self, hashed_item, item):
        if item:
            return bcrypt.checkpw(item.encode('utf-8'), hashed_item)
        else:
            return False
     
    def create_user(self):
        password = self.hash_creator(self.cad_password.get())
        response = self.hash_creator(self.cad_response.get())
        
        mg = DbAccess()
        sucess, error = mg.create_user(self.cad_user.get(), password,
                               self.cad_question.get(), response)
        if sucess:
            messagebox.showinfo("Atenção", "Usuário criado com sucesso!")
            mg.close_connection()
            self.show_login()
        else:
            messagebox.showerror("Erro", f"Erro ao criar usuário: {error}") 
            mg.close_connection()  
            
    def valid_login(self):
        username = self.entry_login_user.get()
        password = self.entry_login_password.get()
        
        db = DbAccess()
        result, e = db.valid_login(username)
        if result:
            if self.check_hashed(result, password):
                self.login_success = True
                db.close_connection()
                self.show_bt_home()
            else:
                db.close_connection()
                self.login_attempts()
        else:
            self.login_attempts(e)
    
    def rec_password(self, code):
        db = DbAccess()
        result, e = db.user_rec(self.rec_user.get())
        if code == 1:
            if result:
                self.rec_question.configure(text=result[0][3])
                self.rec_question.pack(pady=20, padx=20)
                self.rec_response.pack(pady=20, padx=20)
                self.bt_recovery.pack(pady=20, padx=20)
                self.voltar.pack_forget()
                self.voltar.pack(pady=20, padx=20)
            else:
                print(f"{result} Usuário inválido.")
        elif code == 2:
           if self.check_hashed(result[0][4], self.rec_response.get()):
                messagebox.showinfo("ATENÇÃO", f"SUA SENHA TEMPORÁRIA É:\n {self.temp_password()}")
           else:
               print("USUARIO RESPOSTA ERRADA")
    
    def temp_password(self):
        caracters = string.ascii_letters + string.digits
        temp_password  =''.join(random.choice(caracters) for _ in range(8))
        return temp_password
    
    def decrypt_db(self):
        pass
    
    def login_attempts(self, e=None):
        if e:
            messagebox.showerror("Erro", f"Erro ao validar dados: {e}\nContate o desenvolvedor YellTech.")
        self.flag_login += 1
        self.show_login()    
        if self.flag_login == 4:
            sys.exit()
    
    def logout(self):
        
        if self.login_success:
            confirm = messagebox.askyesno("Confirmação", "Deseja fazer logout?")
            if confirm:
                self.login_success = False
                self.flag_login = 0
                self.show_login()
        else:
            confirm = messagebox.askyesno("Confirmação", "Deseja fechar o programa?")
            if confirm:
                sys.exit()
        
    def clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()
            
    def toggle_password(self, entry):
        pass       

if __name__ == "__main__":
    app = App()
    app.mainloop()
