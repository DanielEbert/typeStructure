struct NestedStruct
{
    float nes;
};

struct MyStruct
{
    int a;
    bool b;
    NestedStruct nest;
    int arr[3];
};

int main(){
    volatile MyStruct s;
    return s.a;
}

