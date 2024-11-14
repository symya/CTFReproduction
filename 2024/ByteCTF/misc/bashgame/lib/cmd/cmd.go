package cmd

import (
        "context"
        "os/exec"
        "time"
)

const ExecTimeout = 5 * time.Second

func Exec(name string, arg ...string) (ret string, err error) {
        var stdout = make([]byte, 0)
        ctx, cancel := context.WithTimeout(context.Background(), ExecTimeout)
        defer cancel()
        cmd := exec.CommandContext(ctx, name, arg...)
        stdout, err = cmd.Output()
        if err != nil {
                return
        }
        ret = string(stdout)
        return
}
