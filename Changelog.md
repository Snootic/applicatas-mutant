## Versão 0.9
### Adições e mudanças
- UI/UX do programa retrabalhada para ser mais responsiva e visualmente agradável. ([#6](https://github.com/Snootic/applicatas-mutant/pull/6))
- Adicionado retornos visuais para erros e tratamento de erros (Telas de erro e mudança de cor nos Fields e Botões). ([2a9df56](https://github.com/Snootic/applicatas-mutant/commit/2a9df565ac26dc673f61b9d2e5aae8ff3be66190)), ([518c592](https://github.com/Snootic/applicatas-mutant/commit/518c59234ffc959dfdc2dbde92ae71b89eefe53b)), ([36e4c9d](https://github.com/Snootic/applicatas-mutant/commit/36e4c9dbcaeaf2f5fefccdd3f79976e4a150e6a3)), ([91b6489](https://github.com/Snootic/applicatas-mutant/commit/91b6489059bd1982a65f43b7049104f8f0aefe10)), ([8ea73af](https://github.com/Snootic/applicatas-mutant/commit/8ea73af9410d5e26fbc438a256d41bf82dd922df)), ([9d8ef97](https://github.com/Snootic/applicatas-mutant/commit/9d8ef97a298c96d1c50e4941f7cdcb3a7567a082))
- Adicionado função de cálculo de distribuição binomial (**Ainda não implementada**). ([#4](https://github.com/Snootic/applicatas-mutant/pull/4))
- Cada usuário agora tem uma pasta única para seus schemas. ([b04f257](https://github.com/Snootic/applicatas-mutant/commit/b04f257dc6185dd13c56e8520324bed4aa725e06))
- Adicionado gráficos distintos de pareto para dados quantitativos e/ou qualitativos. ([#3](https://github.com/Snootic/applicatas-mutant/pull/3))
- Adicionado Campos e botões para deletar tabelas e dados de uma tabela. ([3ee3ed7](https://github.com/Snootic/applicatas-mutant/commit/3ee3ed76fb812f5a03733044c3a5bf64add073fc)), ([5914ec2](https://github.com/Snootic/applicatas-mutant/commit/5914ec2eb4034051331ab686b12914aac01bb78e))
- Modificado função de alterar dados de uma tabela de pareto.([0446025](https://github.com/Snootic/applicatas-mutant/commit/04460256b6d63f64f82766f2dfd55b92e3772f98))
- Adicionado novos assets para tela de registro. ([5ace674](https://github.com/Snootic/applicatas-mutant/commit/5ace674ee19306a526d1676b537f64cecd3bc497)), ([2205c85](https://github.com/Snootic/applicatas-mutant/commit/2205c8514dd6fbefb1c4073692f0010642d5573a))
- Adicionado novos tipos de botões. ([ca6014f](https://github.com/Snootic/applicatas-mutant/commit/ca6014f0c8a85e42ce2e109e1554ca52582dd0ad))
- O tema agora pode ser mudado a partir da tela de login. ([1cca645](https://github.com/Snootic/applicatas-mutant/commit/1cca645fb2deab35d581ec35d89fbfe1ed0ac2e9))
- Modificada a função de salvar arquivos, movendo-a para um script próprio. ([#2](https://github.com/Snootic/applicatas-mutant/pull/2))
- Widgets e fontes agora se auto ajustam de acordo com o tamanho da tela.([7fa88b6](https://github.com/Snootic/applicatas-mutant/commit/7fa88b68ce08dbc4a636af09932b7f6b8ca97f88))
- Diversas outras adições menores

### Correções
- Ao criar uma tabela nova, se a mesma já existir, o programa a abre, carregando os dados já existentes. ([ec7a79b](https://github.com/Snootic/applicatas-mutant/commit/ec7a79bd7423b465c7fa9b2b700495fd30b1983a))
- [WinError 32] when saving table changes [#1](https://github.com/Snootic/applicatas-mutant/issues/1). ([#2](https://github.com/Snootic/applicatas-mutant/pull/2))
- Bug no diálogo confirmação de alterações onde ao tentar fechar o programa, o mesmo fechava ao pressionar o botão cancelar. ([#2](https://github.com/Snootic/applicatas-mutant/pull/2))
- Aplicativo não fecha se não houveram mudanças nas tabelas ou se elas já foram salvas. ([#3](https://github.com/Snootic/applicatas-mutant/pull/3))
- Organiza tabelas de pareto qualitativas corretamente e corrige alguns bugs relacionados. ([#3](https://github.com/Snootic/applicatas-mutant/pull/3))
- Outros bugs menores.