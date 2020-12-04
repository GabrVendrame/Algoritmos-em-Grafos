#include <stdio.h>
#include <stdlib.h>

#define ordem 5;
#define nulo -1;

typedef struct cabeca{
    int rrnraiz;
} cabecalho;

typedef struct pag{
    int qntchave;
    int chaves[ordem - 1];
    int filhos[ordem];
} pagina;

enum{sem_promo, promo, insercao, erro};
enum{nao_encontrou, encontrou};

void ler_pag(int rrn, pagina *p, FILE *arvoreb){
    int offset = sizeof(cabecalho) + rrn * sizeof(pagina);
    fseek(arvoreb, offset, SEEK_SET);
    fread(p, sizeof(pagina), 1, arvoreb);
}

void escreve_pag(int rrn, pagina *p, FILE *arvoreb){
    int offset = sizeof(cabecalho) + rrn * sizeof(pagina);
    fseek(arvoreb, offset, SEEK_SET);
    fwrite(p, sizeof(pagina), 1, arvoreb);    
}

int rrn_novo(FILE *arvoreb){
    int offset;
    fseek(arvoreb, 0, SEEK_END);
    offset = ftell(arvoreb);
    return (offset = sizeof(cabecalho)/sizeof(pagina));
}

void inicia_pag(pagina *p){
    int i = 0;
    while(i < ordem - 1){
        pag -> chaves[i] = nulo;
        pag -> filhos[i] = nulo;
        i++;
    }
    pag -> filhos[i] = nulo;
    pag -> qntchaves = 0;
}

int pos_chaves(int chave, int chaves[], int qtnchaves){
    int i = 0;
    while(i < qntchaves && chaves[i] < chave){
        i++;
    }
    return i;
}

void insere_chave_promo(int chavepromo, int rrnpromo, int chaves[], int filhos[], int *qntchaves){
    int pos;
    pos = pos_chaves(chavepromo, chaves, *qntchaves);
    int i = *qntchaves;
    while(i > pos){
        chaves[i] = chaves[i - 1];
        filhos[pos + 1] = filhos[i];
        i--;
    }
    chaves[pos] = chavepromo;
    filhos[pos + 1] = rrnpromo;
    (*qntchaves)++;
}

void divide(int chave, int filho_d, pagina *p, int *chavepromo, int *filho_d_promo, pagina *novap, FILE *arvoreb){
	int pagaux_chaves[ordem], pagaux_filhos[ordem+1], pagaux_num_chaves, i = 0, mediana;
    // copiando pagina para uma pagina auxiliar
	while(i < p -> qntchaves){
		pagaux_chaves[i] = p -> chaves[i];
		pagaux_filhos[i] = p -> filhos[i];
        i++;
	}
	pagaux_filhos[i] = p -> filhos[i];
	pagaux_num_chaves = p -> num_chaves;
	// Inserir CHAVE e FILHO_D  em PAGAUX
	insere_chave_promo(chave, filho_d, pagaux_chaves, pagaux_filhos, &(pagaux_num_chaves));
	inicia_pag(novap);
	inicia_pag(p);
	// CHAVE_PRO recebe a mediana de PAGAUX
	mediana = pagaux_num_chaves/2;
	*chavepromo = pagaux_chaves[mediana];
	// Copiar as chaves e ponteiros para os locais adequados
	while(i < mediana){
		p -> chaves[i] = pagaux_chaves[i];
		p -> filhos[i] = pagaux_filhos[i];
		p -> qntchaves++;
        i++;
	}
	p -> filhos[i] = pagaux_filhos[i];
	for(i = mediana+1; i < pagaux_num_chaves; i++){
		novap -> chaves[novap->qntchaves] = pagaux_chaves[i];
		novap -> filhos[novap->qntchaves] = pagaux_filhos[i];
		novap -> qntchaves++;
	}
	novap->filhos[novap->qntchaves] = pagaux_filhos[i];
	// FILHO_D_PRO  recebe o novo RRN
	*filho_d_pro = rrn_novo(arvoreb);
}

int insere(int rrn, int chave, int *chavepromo, int *filho_d_pro, FILE *arvoreb){
    pagina p, novap;
    int chavepro, rrnpromo, pos, retorno;
    if(rrn == nulo){
        *chavepromo = chave;
        *filho_d_pro = nulo;
        return promo;
    }
    ler_pag(rrn, &p, arvoreb);
    pos = pos_chaves(chave, p.chaves, p.qntchave);
    if(pos < p.qntchaves && p.chaves[pos] == chave){
        return erro;
    }
    retorno = insere(p.filhos[pos], chave, &chavepro, &rrnpromo, arvoreb);
    if(retorno == sem_promo || retorno = erro){
        return retorno;
    }
    else{
        if(p.qntchave < ordem - 1){
            insere_chave_promo(chavepro, rrnpromo, p.chaves, p.filhos, &(p.qntchave));
            escreve_pag(rrn, &p, arvoreb);
            return sem_promo;
        }
        else{
            divide(chavepro, rrnpromo, &p, chavepromo, filho_d_pro, &novap, arvoreb);
            escreve_pag(rrn, &p, arvoreb);
            escreve_pag(*filho_d_pro, &novap, arvoreb);
            return promo;
        }
    }
}

int insere_chave(int chave, int *rrn, FILE *arvoreb){
    pagina raiz;
    int chavepro, filho_d_pro, retorno;
    retorno = insere(*rrn, chave, &chavepro, &filho_d_pro, arvoreb);
    if(retorno == erro){
        return erro;
    }
    else if(retorno == promo){
        pagina raiznova;
        inicia_pag(&raiznova);
        raiznova.chaves[0] = chavepro;
        raiznova.filhos[0] = *rrn;
        raiznova.filhos[1] = filho_d_pro;
        raiznova.qntchave = 1;
        *rrn = rrn_novo(arvoreb);
        escreve_pag(*rrn, &raiznova, arvoreb);
    }
    return insercao;
}

int le_chave(FILE *f, int *chave){
    return fscanf(f, %d, chave);
}

void cria_arv(char *nome){
    FILE *chave, *arvoreb;
    int cont, i, chave;
    char buffer[500];
    cabecalho cab;
    pagina raiz;
    if((chaves = fopen(nome, "rb")) == NULL ){
        printf("ERRO: arquivo dados.dat nao encontrado \n");
    }
    if((arvoreb = fopen("btree.dat", "w+b")) == NULL){
        printf("ERRO: nao foi possivel criar o arquivo btree.dat \n");
    }
    cab.rrnraiz = 0;
    fwrite(&cab, sizeof(cabecalho), 1, arvoreb);
    inicia_pag(&raiz);
    escreve_pag(cab.rrnraiz, &raiz, arvoreb);
    while(le_chave(chaves, &chave) > 0){
        if(insere_chave(chave, &(cab.rrnraiz), arvoreb) == erro){
            printf("ERRO: chave %d ja existe no arquivo", chave);
        }
    }
    fseek(arvoreb, 0, SEEK_SET);
    fwrite(&cab, sizeof(cabecalho), 1, arvoreb);
    fclose(chaves);
    fclose(arvoreb);
}

// void imprime(FILE *arvoreb); fazer esse aqui nois memo;
// int altura(FILE *arvoreb); fazer nois memo;
// void estatisticas(FILE *arvoreb); fazer;
// void relatorio(); fazer;


// int main(int argc, char **argv) {

//     if (argc < 2) {
//         fprintf(stderr, "Numero incorreto de argumentos!\n");
//         fprintf(stderr, "Modo de uso:\n");
//         fprintf(stderr, "$ %s -c arquivo_chaves\n", argv[0]);
//         fprintf(stderr, "$ %s -p\n", argv[0]);
//         exit(1);
//     }

//     if (strcmp(argv[1], "-c") == 0) {
//         printf("Criando Arvore-B... Arvore-B criada com sucesso \n", argv[2]);
//     } else if (strcmp(argv[1], "-p") == 0) {
//    
//     } else {
//         fprintf(stderr, "Opcao \"%s\" nao suportada!\n", argv[1]);
//     }

//     return 0;
