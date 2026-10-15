**Só saber que o aplicativo é web não permite escolher uma única opção correta.** VM, contêineres e App Service podem hospedar aplicações web.

Se você precisa de uma indicação agora, eu começaria por **Azure App Service**, supondo que a aplicação seja compatível e que você queira reduzir a administração da infraestrutura. É uma recomendação condicional:

- **App Service:** para hospedar a aplicação em uma plataforma gerenciada.
- **VM:** quando é necessário controlar ou personalizar o sistema operacional.
- **Contêineres:** quando empacotar a aplicação e suas dependências é um requisito; ainda é preciso escolher onde executá-los.

Essas opções aparecem na [explicação oficial da Microsoft sobre hospedagem](https://learn.microsoft.com/en-us/training/modules/describe-azure-compute-networking-services/7-describe-application-hosting-options).

Para o AZ-900, procure o requisito que decide a escolha: “é web” sozinho deixa a questão ambígua. **Seu aplicativo precisa instalar ou configurar algo diretamente no sistema operacional?**
