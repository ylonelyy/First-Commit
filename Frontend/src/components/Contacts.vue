<template>
  <div class="contacts">
    <h1>Lista de Contatos</h1>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Carregando contatos...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <h3>Erro ao carregar contatos</h3>
      <p>{{ error }}</p>
      <button @click="loadContacts" class="retry-btn">Tentar Novamente</button>
    </div>
    
    <div v-else-if="contacts.length === 0" class="empty-state">
      <p>Nenhum contato encontrado.</p>
    </div>
    
    <ul v-else>
      <li v-for="contact in contacts" :key="contact.email || contact._id" class="contact-item">
        <div class="avatar">
          <img 
            :src="contact.photo || 'https://via.placeholder.com/50/007bff/ffffff?text=U'" 
            alt="Foto" 
            class="avatar-img"
            @error="handleImageError"
          />
        </div>
        <div class="contact-info">
          <strong class="contact-name">{{ contact.name || 'Nome não informado' }}</strong>
          <span class="contact-email">{{ contact.email || 'E-mail não informado' }}</span>
          <span class="contact-phone" v-if="contact.phone">{{ contact.phone }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "Contacts",
  data() {
    return {
      contacts: [],
      loading: true,
      error: null
    }
  },
  mounted() {
    this.loadContacts()
  },
  methods: {
    async loadContacts() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get("http://localhost:5000/contacts")
        
        // Verifica se a resposta tem a estrutura esperada
        if (response.data && response.data.contacts) {
          this.contacts = response.data.contacts
        } else {
          console.error("Estrutura de resposta inesperada:", response.data)
          this.error = "Formato de dados inesperado do servidor"
        }
      } catch (err) {
        console.error("Erro ao carregar contatos:", err)
        
        if (err.response) {
          // O servidor respondeu com um status de erro
          if (err.response.status === 404) {
            this.error = "Endpoint não encontrado. Verifique a URL da API."
          } else {
            this.error = `Erro ${err.response.status}: ${err.response.data.error || 'Erro desconhecido'}`
          }
        } else if (err.request) {
          // A requisição foi feita mas não houve resposta
          this.error = "Não foi possível conectar ao servidor. Verifique se o Flask está rodando."
        } else {
          // Outro tipo de erro
          this.error = `Erro: ${err.message}`
        }
      } finally {
        this.loading = false
      }
    },
    handleImageError(event) {
      // Fallback para imagem quebrada
      event.target.src = 'https://via.placeholder.com/50/6c757d/ffffff?text=U'
    }
  }
}
</script>

<style scoped>
.contacts {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  text-align: center;
  padding: 30px;
  background-color: #ffebee;
  border-radius: 8px;
  color: #c62828;
}

.error h3 {
  margin-top: 0;
}

.retry-btn {
  margin-top: 15px;
  padding: 8px 16px;
  background-color: #c62828;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.retry-btn:hover {
  background-color: #b71c1c;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.contact-item {
  display: flex;
  align-items: center;
  padding: 15px;
  margin-bottom: 10px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.contact-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.avatar {
  margin-right: 15px;
  flex-shrink: 0;
}

.avatar-img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.contact-info {
  display: flex;
  flex-direction: column;
}

.contact-name {
  font-size: 16px;
  color: #2c3e50;
  margin-bottom: 4px;
}

.contact-email {
  font-size: 14px;
  color: #7f8c8d;
  margin-bottom: 2px;
}

.contact-phone {
  font-size: 14px;
  color: #3498db;
}
</style>