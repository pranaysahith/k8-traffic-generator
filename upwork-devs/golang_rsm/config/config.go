package config

import (
	"os"
	"time"

	"github.com/spf13/viper"
)

//Config is
func Config() (time.Duration, string) {
	if os.Getenv("ENVIROMENT") == "DEV" {
		viper.SetConfigName("config")
		viper.SetConfigType("toml")
		viper.AddConfigPath("github.com/tgg")
		viper.ReadInConfig()
	} else {
		viper.AutomaticEnv()
	}
	timeout := viper.GetDuration("app_timeout")
	urlfile := viper.GetString("url_file")
	return timeout, urlfile
}
