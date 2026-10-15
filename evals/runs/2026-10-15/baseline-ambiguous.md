**Com apenas “é web”, não existe uma única resposta correta.** VM, container e App Service podem hospedar aplicações web.

Se você precisa de uma escolha inicial, eu escolheria **Azure App Service**, assumindo que seu aplicativo usa um runtime compatível e que você quer evitar administrar o sistema operacional. É uma recomendação provisória, não uma conclusão garantida.

Para o AZ-900, procure a necessidade no enunciado:

- **App Service:** hospedar uma aplicação web em uma plataforma gerenciada.
- **Container:** executar uma aplicação empacotada com suas dependências; ainda é preciso escolher onde executar esse container.
- **VM:** ter controle do sistema operacional, assumindo sua administração e atualizações.

Seu aplicativo exige controle do sistema operacional ou alguma dependência específica?
