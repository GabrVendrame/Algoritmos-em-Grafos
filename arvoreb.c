#include <stdio.h>
#include <stdlib.h>

#define ordem 5;
#define nulo -1;

typedef struct cabeca{
    int rrn;
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

// int main(int argc, char **argv) {

//     if (argc < 3) {
//         fprintf(stderr, "Numero incorreto de argumentos!\n");
//         fprintf(stderr, "Modo de uso:\n");
//         fprintf(stderr, "$ %s (-c|-p) nome_arquivo\n", argv[0]);
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
