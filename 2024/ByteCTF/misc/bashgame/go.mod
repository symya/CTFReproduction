module bashgame
require (
        github.com/gin-gonic/gin latest
        ByteCTF/lib/cmd v0.0.0
)
go 1.20
replace ByteCTF/lib/cmd => /app/lib/cmd
