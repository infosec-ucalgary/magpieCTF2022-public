package auth

import (
	"log"
	"strings"
	"io/ioutil"
	"fmt"

	"github.com/golang-jwt/jwt/v4"
)

func GetSecretKey() ([]byte, error) {
	file, err := ioutil.ReadFile("a_secret.key")
	if err != nil {
		panic("Cannot open secret key file")
	}
	return file, err
}

func fatal(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

type CustomerInfo struct {
	Username string
	Kind string
}

type CustomClaimsInfo struct {
	*jwt.StandardClaims
	TokenType string
	CustomerInfo
}

func TrimAndParseToken(tokBuffer []byte) (string, error) {
	tokenString := strings.TrimSpace(string(tokBuffer[:]))
	tokenString = tokenString[7:]
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"])
		}
		return []byte("This is a super great secret key :)"), nil
	})

	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		return claims["username"].(string), nil
	} else {
		return "", err
	}
}
