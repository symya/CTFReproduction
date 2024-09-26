package main

import (
        "ByteCTF/lib/cmd"

        "github.com/gin-gonic/gin"
)

func main() {
        r := gin.Default()
        r.POST("/update", func(c *gin.Context) {
                result := Update(c)
                c.String(200, result)
        })
        r.GET("/", func(c *gin.Context) {
                c.String(200, "Welcome to BashGame")
        })
        r.Run(":23333")
}

const OpsPath = "/opt/challenge/ops.sh"
const CtfPath = "/opt/challenge/ctf.sh"

func Update(c *gin.Context) string {
        username := c.PostForm("name")
        if len(username) < 6 {
                _, err := cmd.Exec("/bin/bash", OpsPath, username)
                if err != nil {
                        return err.Error()
                }
        }
        ret, err := cmd.Exec("/bin/bash", CtfPath)
        if err != nil {
                return err.Error()
        }
        return string(ret)
}
