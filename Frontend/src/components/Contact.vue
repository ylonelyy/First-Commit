<script>
    export default {
        name: 'Contact',
        props: {
            contact: {
                type: Object,
                required: true
            }
        }
    }
</script>

<template>
    <!-- Este componente exibe um contato. -->
        <div>
            <img :src="contact.photo" alt="contact.name" />
            <div class="contact-info">
            <p>{{ contact.name }}</p>
            <p>{{ contact.email }}</p>
            </div>
        </div>
</template>

<style scoped>

img {

border-radius: 50%;

width: 50px;

height: 50px;

margin-right: 10px;

}

p {

margin: 0;

display: inline-block;

margin-left: 10px;

}

div {

display: flex;

align-items: center;

justify-content: flex-start;

padding: 10px;

margin: 10px;

border: 1px solid #ffffff; /* Adiciona uma
borda cinza */

border-radius: 5px; /* Adiciona cantos
arredondados */

transition: all 0.3s ease; /* Adiciona uma
transição suave */

}

</style>